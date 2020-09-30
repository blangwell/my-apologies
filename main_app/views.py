from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.decorators import method_decorator
from django.db.models.signals import pre_save
from main_app.models import set_username, Account, Apology
from main_app.forms import RegistrationForm, AccountAuthenticationForm, ApologyForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator

def index(request):
  return render(request, 'index.html')

def about(request):
  return render(request, 'about.html')

@login_required
def profile(request, email):
  user = Account.objects.get(email=email)
  apologies = Apology.objects.filter(user=user)
  return render(request, 'profile.html', {'email': email, 'apologies': apologies})

@login_required
def settings(request, email):
  user = Account.objects.get(email=email)
  return render(request, 'settings.html', {'user': user})

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
        return HttpResponseRedirect('/account/' + str(request.user))


  else:
    form = AccountAuthenticationForm()

  context['login_form'] = form
  return render(request, 'login.html', context)

''' 
NOTE: the change_password does not require class inheritence
so i have included it as a views function 
'''
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
      messages.warning(request, 'Error changing password!')
  else:
    form = PasswordChangeForm(request.user)
  return render(request, 'change_password.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class DisplayNameUpdate(UpdateView):
    model = Account
    fields = ['display_name']

    def form_valid(self, form):
      self.object = form.save(commit=False)
      self.object.user = self.request.user
      self.object = form.save()
      
      return HttpResponseRedirect(f'/account/{str(self.object.user)}/settings')

# @login_required
# def display_name_update(request):
  
  

###### APOLOGY #######
@login_required
def write_apology_letter(request):
  # user = request.user
  form = ApologyForm(request.POST or None)
  form.instance.user = request.user
  if form.is_valid():
    # obj = form.save(commit=False)
    form.save()
    return HttpResponseRedirect('/account/' + str(request.user))
  
  context = {
    'form': form,
    'user': form.instance.user
  }
  return render(request, 'apology.html', context)

@method_decorator(login_required, name='dispatch')
class ApologyLetterUpdate(UpdateView):
  model = Apology
  fields = ['post_text', 'public']

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.save()
    return HttpResponseRedirect(f'/account/{str(self.object.user)}')


@method_decorator(login_required, name='dispatch')
class ApologyLetterDelete(DeleteView):
  model = Apology
  def get_success_url(self):
    return reverse_lazy('profile', kwargs={'email': self.request.user})

def apology_show(request, apology_id):
  apology = Apology.objects.get(id=apology_id)
  return render(request, 'apologies/show.html', {'apology': apology})

def apology_index(request):
  # we must order_by a unique field (id) and then the date updated to prevent dupes in pagination
  apologies = Apology.objects.filter(public=True).order_by('id', 'updated_at')
  paginator = Paginator(apologies, 1)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  return render(request, 'apologies/index.html', {'apologies': apologies, 'page_obj': page_obj})