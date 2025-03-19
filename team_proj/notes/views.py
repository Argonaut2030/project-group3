from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

from .forms import TagForm, NoteForm
from .models import Tag, Note


@login_required
def notes_home(request):
    return render(request, 'notes/index.html')

@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            user = request.user
            if Tag.objects.filter(user=user, name=name).exists():
                messages.error(request, f"Тег з ім'ям '{name}' уже існує.")
                return render(request, 'notes/add_tag.html', {'form': form})
            else:
                tag = form.save(commit=False)
                tag.user = user
                tag.save()
                messages.success(request, f"Тег '{name}' успішно додано.")
                return redirect(to='notes:notes_home')
        else:
            return render(request, 'notes/add_tag.html', {'form': form})
    else:
        form = TagForm()
        return render(request, 'notes/add_tag.html', {'form': form})

@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            # Додаємо обрані існуючі теги
            for tag in form.cleaned_data['existing_tags']:
                note.tags.add(tag)

            # Додаємо новий тег, якщо введено
            new_tag_name = form.cleaned_data.get('new_tag')
            if new_tag_name:
                new_tag, created = Tag.objects.get_or_create(
                    user=request.user, name=new_tag_name
                )
                note.tags.add(new_tag)

            note.save()
            return redirect('notes:notes_home')
    else:
        form = NoteForm(user=request.user)

    return render(request, 'notes/add_note.html', {'form': form})

@login_required
def search_notes(request):
    query = request.GET.get('q')
    if query:
        notes = Note.objects.filter(user=request.user, name__icontains=query).order_by('name')
    else:
        notes = Note.objects.filter(user=request.user).order_by('name')

    paginator = Paginator(notes, 10)
    page_number = request.GET.get('page')
    notes = paginator.get_page(page_number)
    return render(request, 'notes/search_results.html', {'notes': notes, 'query': query})

@login_required
def detail_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id,user=request.user)
    return render(request, 'notes/detail_note.html', {"note": note})


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note, user=request.user)
        if form.is_valid():
            note = form.save()

            # Оновлюємо зв'язки з тегами
            note.tags.clear()
            for tag in form.cleaned_data['existing_tags']:
                note.tags.add(tag)

            new_tag_name = form.cleaned_data.get('new_tag')
            if new_tag_name:
                new_tag, created = Tag.objects.get_or_create(
                    user=request.user, name=new_tag_name
                )
                note.tags.add(new_tag)

            return redirect('notes:notes_home')
    else:
        form = NoteForm(instance=note, user=request.user)

    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})

@login_required
def delete_note(request, note_id):
    note = Note.objects.filter(id=note_id, user=request.user).first()
    if not note:
        messages.error(request, 'Note not found.')
        return redirect('notes:notes_home')

    note.delete()
    messages.success(request, 'Note deleted successfully.')
    return redirect('notes:notes_home')

def main(request, page = 1):
    if not request.user.is_authenticated:
        return render(request, 'notes/index.html', {'user_authenticated': False})

    notes = Note.objects.filter(user=request.user).order_by('name')
    per_page = 3
    paginator = Paginator(notes, per_page)
    notes_on_page = paginator.page(page)
    return render(request, 'notes/index.html', {'notes': notes_on_page, 'user_authenticated': True})