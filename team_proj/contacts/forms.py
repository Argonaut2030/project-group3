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