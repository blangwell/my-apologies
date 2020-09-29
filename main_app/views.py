from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models.signals import pre_save
from main_app.models import set_username, Account
from main_app.forms import RegistrationForm, AccountAuthenticationForm


def index(request):
  return render(request, 'index.html')

def about(request):
  return render(request, 'about.html')

@login_required
def profile(request, email):
  account = Account.objects.get(email=email)
  return render(request, 'profile.html', {'email': email})

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

@login_required
def change_password(request):
  if request.method == 'POST':
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
      user = form.save()
      update_session_auth_hash(request, user)
      messages.success(request, 'Your password was successfully updated')
      return redirect('index')
    else:
      messages.error(request, 'Error changing password!')
  else:
    form = PasswordChangeForm(request.user)
  return render(request, 'change_password.html', {'form': form})