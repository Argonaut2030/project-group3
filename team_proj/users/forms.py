from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=16, min_length=3, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=25, required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=16, min_length=3, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ['username', 'password']