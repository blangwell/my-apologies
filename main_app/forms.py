from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate
from taggit.forms import TagWidget

from main_app.models import Account
from main_app.models import Apology

class RegistrationForm(UserCreationForm):
  email = forms.EmailField(max_length=60, help_text='Please enter a valid email address')
  class Meta:
    model = Account
    fields = ("email", "password1", "password2")


class AccountAuthenticationForm(forms.ModelForm):
  password = forms.CharField(label='Password', widget=forms.PasswordInput)

  class Meta:
    model = Account
    fields = ("email", "password")

  def clean(self): # before the form can do anything, we need to run this clean method
    if self.is_valid():
      email = self.cleaned_data['email']
      password = self.cleaned_data['password']
      if not authenticate(email=email, password=password):
        raise forms.ValidationError('Email or Password is incorrect')

class ApologyForm(forms.ModelForm):
  class Meta:
    model = Apology
    
    fields = [
      'post_text',
      'public',
      'tags'
    ]
    widgets = {
      'tags': TagWidget()
    }


# class TagForm(forms.Form):
#   tag = forms.CharField(label='Tag', max_length=100)