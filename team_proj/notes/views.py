from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

from .forms import TagForm, NoteForm
from .models import Tag, Note


@login_required
def notes_home(request):
    return render(request, 'notes/index.html')

def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='notes:notes_home')
        else:
            return render(request, 'notes:tag.html', {'form': form})
        """Не забути поміняти шлях Noteapp/tag.html"""

    return render(request, 'noteapp/tag.html', {'form': TagForm()})


@login_required
def add_note(request):
    note_form = NoteForm()
    tag_form = TagForm()

    if request.method == 'POST':
        note_form = NoteForm(request.POST)
        tag_form = TagForm(request.POST)

        if note_form.is_valid() and tag_form.is_valid():
            tag = tag_form.save() #save tag
            note = note_form.save(commit=False) #save note, but do not save many to many relationships yet
            note.user = request.user
            note.save()
            note.tags.add(tag) #add the tag to the note.
            messages.success(request, 'Note and Tag added successfully.')
            return redirect('notes:notes_home')
        else:
            messages.error(request, 'Error adding note and tag. Please correct the errors.')

    return render(request, 'notes/add_note.html', {'note_form': note_form, 'tag_form': tag_form})

@login_required
def search_notes(request):
    query = request.GET.get('q')
    if query:
        notes = Note.objects.filter(user=request.user, name__icontains=query)
    else:
        notes = Note.objects.filter(user=request.user)

    paginator = Paginator(notes, 10)
    page_number = request.GET.get('page')
    notes = paginator.get_page(page_number)

    return render(request, 'notes/search_notes.html', {'notes': notes, 'query': query})

def detail_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, 'notes/detail_note.html', {"note": note})

@login_required
def edit_note(request, note_id):
    note = Note.objects.filter(id=note_id, user=request.user).first()
    if not note:
        messages.error(request, 'Note not found.')
        return redirect('notes:notes_home')

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully.')
            return redirect('notes:notes_home')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form})

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