from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Contact

def validate_phone(value):
    if not re.match(r'^\+?1?\d{9,12}$', value):
        raise ValidationError('The phone number must contain between 10 and 13 characters.')


class ContactForm(forms.ModelForm):
    phone = forms.CharField(validators=[validate_phone])

    class Meta:
        model = Contact
        fields = ['name', 'address', 'phone', 'email', 'birthday']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        # Ігноруємо свій власний об'єкт, якщо він редагується
        qs = Contact.objects.filter(user=self.user, email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('This email is already used by another contact.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        qs = Contact.objects.filter(user=self.user, phone=phone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('This phone number is already used by another contact.')
        return phone
