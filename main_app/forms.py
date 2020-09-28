from django import forms
from django.contrib.auth.forms import UserCreationForm

from main_app.models import Account

class RegistrationForm(UserCreationForm):
  email = forms.EmailField(max_length=60, help_text='Please enter a valid email address')
  class Meta:
    model = Account
    fields = ("email", "password1", "password2")