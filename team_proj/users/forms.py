from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput()
    )

    email = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.EmailInput()
    )

    password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput()
    )

    password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Користувач із таким email вже існує.")
        return email


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']