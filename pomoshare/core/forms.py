from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ModifiedUserModel


class NewUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    password2 = None

    class Meta:
        model = ModifiedUserModel
        fields = ("username", "full_name", "email", "password1")