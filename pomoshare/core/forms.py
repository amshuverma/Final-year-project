from dataclasses import field
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import ModifiedUserModel


class NewUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    password2 = None

    def save(self, commit=True):
        user = super().save(commit=False)
        _full_name_length = len(self.cleaned_data.get('full_name'))
        if _full_name_length > 1:
            user.first_name = self.cleaned_data.get('full_name').strip().split()[0]
            user.last_name = self.cleaned_data.get('full_name').strip().split().pop()
        else:
            user.first_name = self.cleaned_data.get('full_name').strip().split()[0]
        if commit:
            user.save()
        return user

    class Meta:
        model = ModifiedUserModel
        fields = ("username", "full_name", "email", "password1")


class CustomSignupForm(SignupForm):
    full_name = forms.CharField(max_length=100)
    field_order = ['full_name', 'username', 'email', 'passsword']

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data.get('full_name').split()[0]
        user.last_name = self.cleaned_data.get('full_name').split()[1]
        user.save()
        return user

