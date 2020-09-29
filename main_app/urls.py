from django.urls import path
from . import views

from main_app.views import (
    registration_view, 
    login_view, 
    logout_view,
    about,
    profile,
    change_password,
)


urlpatterns = [
  path('', views.index, name='index'),
  path('register/', registration_view, name='register'),
  path('login/', login_view, name='login'),
  path('logout/', logout_view, name='logout'),
  path('about/', about, name='about'),
  path('account/<email>', profile, name='profile'),
  path('password/', change_password, name='change_password')
]