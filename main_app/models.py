from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from taggit.managers import TaggableManager

# class Tag (models.Model):
#   tag_name = models.CharField(max_length=25)
#   # ManyToManyField specifies a N:M relationship, many posts can have many tags

#   def __str__(self):
#     return self.tag_name

#### CUSTOM USER ####

''' 
An alternative user manager for use with our custom 
Account class
'''

class MyAccountManager(BaseUserManager):
  def create_user(self, email, password=None):
    if not email:
      raise ValueError('Please enter a valid email address')
    user = self.model(
      # normalize email converts all chars to lowercase
      email=self.normalize_email(email),
    )
    user.set_password(password)
    user.save(using=self._db)
    return user
  

  def create_superuser(self, email, password):
    user = self.create_user(
      email=self.normalize_email(email),
      password=password,
    )
    user.is_admin = True
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user

''' 
We subclass AbstractBaseUser so that we can create a
completely new User model from scratch with new fields
'''

class Account(AbstractBaseUser):
  email = models.EmailField(verbose_name="email", max_length=60, unique=True)
  display_name = models.CharField(max_length=30, default='Anonymous')
  user_tags = models.CharField(max_length=1500, blank=True, null=True)


  # The following fields are required by AbstractBaseUser to create custom User model.
  username = models.CharField(max_length=30, unique=True)
  date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
  last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)

  # instead of username, login with email
  USERNAME_FIELD = 'email'

  objects = MyAccountManager()

  def __str__(self):
    return self.email

  def has_perm(self, perm, obj=None):
    return self.is_admin

  def has_module_perms(self,app_label):
    return True

def set_username(sender, instance, **kwargs): # **kwargs pass keyworded variable length of args to this function
  if not instance.username:
    instance.username = instance.email




class Apology(models.Model):
  post_text = models.TextField()
  public = models.BooleanField(default=False)
  # ForeignKey is used for 1:M relationships, one user can have many posts
  user = models.ForeignKey(Account, on_delete=models.CASCADE)
  # tags = models.ManyToManyField(Tag)
  tags = TaggableManager(blank=True)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)

  def __str__(self):
    return self.post_text

  def post_is_public(self):
    return self.public

