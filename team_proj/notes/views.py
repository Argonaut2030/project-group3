from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q, Min
import itertools  # Додайте цей імпорт

from .forms import  NoteForm
from .models import Tag, Note


@login_required
def notes_home(request):
    return render(request, 'notes/index.html')


@login_required
def add_note(request):
    note_form = NoteForm()

    if request.method == 'POST':
        note_form = NoteForm(request.POST)

        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.user = request.user
            note.save()

            note_form.save_m2m()  # Save the existing tags FIRST

            # Handle new tags
            new_tags = note_form.cleaned_data.get('new_tags')
            for tag_name in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                note.tags.add(tag)

            messages.success(request, 'Note and Tags added successfully.')
            return redirect('notes:notes_home')
        else:
            messages.error(request, 'Error adding note and tags. Please correct the errors.')

    return render(request, 'notes/add_note.html', {'note_form': note_form})





@login_required
def search_notes(request):
    query = request.GET.get('q')
    if query:
        notes = Note.objects.filter(user=request.user, name__icontains=query)
        notes = Note.objects.filter(user=request.user, name__icontains=query)
    else:
        notes = Note.objects.filter(user=request.user)

    paginator = Paginator(notes, 10)
    page_number = request.GET.get('page')
    notes = paginator.get_page(page_number)

    return render(request, 'notes/search_notes.html', {'notes': notes, 'query': query})
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

def edit_note(request, note_id):
    note = Note.objects.filter(id=note_id, user=request.user).first()
    if not note:
        messages.error(request, 'Note not found.')
        return redirect('notes:notes_home')

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully.')
            return redirect('notes:notes_home')
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

@login_required
def main(request, page = 1):
    if not request.user.is_authenticated:
        return render(request, 'notes/index.html', {'user_authenticated': False})

    query = request.GET.get('q')
    sort_by = request.GET.get('sort')
    notes = Note.objects.filter(user=request.user)

    if query:
        notes = notes.filter(tags__name__icontains=query)

    if sort_by == 'tags':
        all_tags = Tag.objects.all().order_by('name')
        grouped_notes = []
        for tag in all_tags:
            notes_with_tag = Note.objects.filter(user=request.user, tags=tag)
            if notes_with_tag.exists(): #Check if notes with this tag exist
                grouped_notes.append({'tag': tag.name, 'notes': notes_with_tag})
        notes = grouped_notes
    elif sort_by:
        notes = notes.order_by(sort_by)

    per_page = 10
    paginator = Paginator(notes, per_page)
    notes_on_page = paginator.page(page)
    return render(request, 'notes/index.html', {'notes': notes_on_page, 'user_authenticated': True, 'query': query, 'sort_by': sort_by})
