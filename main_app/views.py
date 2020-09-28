from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from main_app.forms import RegistrationForm
from django.db.models.signals import pre_save
from main_app.models import set_username, Account

# Create your views here.
def index(request):
  return render(request, 'index.html')

def registration_view(request):
  context = {}
  if request.POST:
    form = RegistrationForm(request.POST)
    if form.is_valid():
      pre_save.connect(set_username, sender=Account)
      form.save()
      email = form.cleaned_data.get('email')
      raw_password = form.cleaned_data.get('password1')
      account = authenticate(email=email, password=raw_password)
      login(request, account)
      return redirect('index')
    else:
      context['registration_form'] = form
  else: # if request is GET request
    form = RegistrationForm()
    context['registration_form'] = form
  return render(request, 'register.html', context)
