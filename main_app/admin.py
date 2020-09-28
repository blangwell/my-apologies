from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main_app.models import Account
from main_app.models import Post

# An admin panel for our custom Account class
class AccountAdmin(UserAdmin):
  list_display = ('email', 'display_name', 'date_joined', 'last_login', 'is_admin', 'is_staff')
  search_fields = ('email', 'tags')
  readonly_fields = ('date_joined', 'last_login')

  filter_horizontal = ()
  list_filter = ()
  fieldsets = ()

admin.site.register(Account, AccountAdmin)
admin.site.register(Post)