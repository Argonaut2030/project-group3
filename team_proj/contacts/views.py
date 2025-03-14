from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime, timedelta

from .forms import ContactForm
from .models import Contact


@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact added successfully.')
            return redirect('contacts:home')
    else:
        form = ContactForm()
    return render(request, 'contacts/add_contact.html', {'form': form})

@login_required
def upcoming_birthdays(request, days=None):
    if request.method == 'POST':
        days = request.POST.get('days')
        if not days:
            messages.warning(request, 'Please enter the number of days.')
            return render(request, 'contacts/upcoming_birthdays.html')

        days = int(days)
        today = datetime.now().date()
        target_date = today + timedelta(days=days)
        contacts = Contact.objects.filter(birthday__month=target_date.month, birthday__day=target_date.day)
        return render(request, 'contacts/upcoming_birthdays.html', {'contacts': contacts, 'days': days})
    return render(request, 'contacts/upcoming_birthdays.html')


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



def main(request, page = 1):
    if not request.user.is_authenticated:
        return render(request, 'contacts/index.html', {'user_authenticated': False})

    contacts = Contact.objects.all().order_by('name')
    per_page = 10
    paginator = Paginator(contacts, per_page)
    contacts_on_page = paginator.page(page)
    return render(request, 'contacts/index.html', {'contacts': contacts_on_page, 'user_authenticated': True})
