from django.urls import path
from . import views
# from django.conf.urls.static import static

from main_app.views import (
    registration_view, 
    login_view, 
    logout_view,
    about,
    profile,
    change_password,
    write_apology_letter,
    ApologyLetterDelete,
    ApologyLetterUpdate,
    # apology_show,
    apology_index,
    settings,
    DisplayNameUpdate,
)


urlpatterns = [
  path('', views.index, name='index'),
  path('register/', registration_view, name='register'),
  path('login/', login_view, name='login'),
  path('logout/', logout_view, name='logout'),
  path('about/', about, name='about'),
  path('password/', change_password, name='change_password'),
  path('apology/create', write_apology_letter, name='apology_create'),
  path('apology/<int:pk>/update/', ApologyLetterUpdate.as_view(), name='apology_update'),
  # path('apology/<int:pk>/update/', apology_letter_update, name='apology_update'),
  path('apology/<int:pk>/delete/', ApologyLetterDelete.as_view(), name='apology_delete'),
  # path('apology/<int:apology_id>', apology_show, name='apology_show'),
  path('apology/index', apology_index, name='apology_index'),
  path('account/<email>', profile, name='profile'),
  path('account/<email>/settings', settings, name='account_settings'),
  path('account/settings/display_name/<int:pk>', DisplayNameUpdate.as_view(), name='update_display_name'),
]