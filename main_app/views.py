from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db.models.signals import pre_save
from main_app.models import set_username, Account
from main_app.forms import RegistrationForm, AccountAuthenticationForm

# Create your views here.
def index(request):
  return render(request, 'index.html')

##### ACCOUNT AUTH VIEWS #######
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


def logout_view(request):
  logout(request)
  return redirect('index')


def login_view(request):
  context = {}
  user = request.user
  if user.is_authenticated:
    # if a user is signed in, should redirect to index
    return redirect('index')
  
  if request.POST:
    form = AccountAuthenticationForm(request.POST)
    if form.is_valid():
      email = request.POST['email']
      password = request.POST['password']
      user = authenticate(email=email, password=password)

      if user:
        login(request, user)
        return redirect('index')

  else:
    form = AccountAuthenticationForm()

  context['login_form'] = form
  return render(request, 'login.html', context)