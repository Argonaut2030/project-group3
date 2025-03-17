from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime, timedelta

from .forms import TagForm, NoteForm
from .models import Tag, Note






# Create your views here.
def main(request, page = 1):
    if not request.user.is_authenticated:
        return render(request, 'notes/index.html', {'user_authenticated': False})
    notes = Note.objects.all().order_by('name')
    per_page = 3
    paginator = Paginator(notes, per_page)
    notes_on_page = paginator.page(page)
    return render(request, 'notes/index.html', {'notes': notes_on_page, 'user_authenticated': True})
   
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='notes:home')
        else:
            return render(request, 'noteapp/tag.html', {'form': form})
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
            return redirect('notes:home')
        else:
            messages.error(request, 'Error adding note and tag. Please correct the errors.')

    return render(request, 'notes/add_note.html', {'note_form': note_form, 'tag_form': tag_form})



@login_required
def search_notes(request):
    query = request.GET.get('q')
    if query:
        notes = Note.objects.filter(name__icontains=query)
    else:
        notes = Note.objects.all()
    return render(request, 'notes/search_notes.html', {'notes': notes})

def detail_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, 'notes/detail_note.html', {"note": note})



def delete_note(request, note_id):
    Note.objects.get(pk=note_id).delete()
    return redirect(to='notes:home')











@login_required
def search_contacts(request):
    query = request.GET.get('q')
    if query:
        contacts = Contact.objects.filter(name__icontains=query)
    else:
        contacts = Contact.objects.all()
    return render(request, 'contacts/search_contacts.html', {'contacts': contacts})

@login_required
def edit_contact(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact updated successfully.')
            return redirect('contacts:home')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/edit_contact.html', {'form': form})

@login_required
def delete_contact(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    contact.delete()
    messages.success(request, 'Contact deleted successfully.')
    return redirect('contacts:home')




