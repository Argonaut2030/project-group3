from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=13, validators=[MinLengthValidator(10, message='The phone number must contain at least 10 characters.'),
                                                        MaxLengthValidator(13, message='The phone number must be a maximum of 13 characters.')],
                             unique=True)
    email = models.EmailField(unique=True)
    birthday = models.DateField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)