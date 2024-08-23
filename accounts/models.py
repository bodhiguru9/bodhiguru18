from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save

from orgss.models import Org, Role

from uuid import uuid4

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, username, password=None):
        if not email:
            raise ValueError("User must have an email address")

        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )        

        user.set_password(password)
        user.save(using = self.db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
            password = password,

        )   

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.user_role = 'super_admin'

        user.save(using = self.db)
        return user


    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True        

class Account(AbstractBaseUser):

    USER_ROLES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User')
    )
    
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    username = models.CharField(max_length= 25, unique = True)
    email = models.EmailField(max_length=70, unique = True)
    password = models.CharField(max_length=100)

    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now_add = True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_superadmin = models.BooleanField(default = False)
    user_role = models.CharField(max_length=20, choices=USER_ROLES, default='user')

    is_email_confirmed = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    org = models.ForeignKey(Org, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True        
    
class UserProfile(models.Model):

    def __str__(self):
        return self.user.email   

    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    quizzes_attempted = models.IntegerField(default=1)
    quiz_score = models.IntegerField(default=1)
    quizzes_streak = models.IntegerField(default=1)
    scenarios_attempted = models.IntegerField(default=1)
    scenarios_attempted_score = models.TextField(null=True, blank=True, default="")
    jadu_attempted = models.IntegerField(default=1, null=True, blank=True)
    jadu_asked = models.IntegerField(default=1, null=True, blank=True)
    bookmarks = models.CharField(blank=True,null=True, max_length=300)
    gender = models.CharField(blank=True, null=True, max_length=10)
    user_scenario_saved = models.CharField(max_length= 250, default= "")
    level = models.IntegerField(default=1)
    city = models.CharField(max_length= 250, default= "")
    user_powerwords = models.TextField(default= "")
    user_weakwords = models.TextField(default = "")
    scenario_attempt_pw = models.TextField(default= "")
    scenario_attempt_ww = models.TextField(default = "")
    pw_competency = models.CharField(max_length= 250, default = "pw")
    ww_competency = models.CharField(max_length=250, default = "ww")
    competency_score = models.TextField(null=True, blank=True)


@receiver(post_save,sender=Account)
def save_profile(sender, instance, created, **kwargs):
    user = instance

    if created:
        profile = UserProfile(user=user)
        profile.save()


class EmailConfirmationToken(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

class Profile(models.Model):
    def __str__(self):
        return self.user.email    

    user = models.OneToOneField(Account, related_name='profile', on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=50, default="", blank= True)
    reset_password_expire = models.DateTimeField(null=True, blank=True)     

@receiver(post_save,sender=Account)
def save_profile(sender, instance, created, **kwargs):
    user = instance

    if created:
        profile = Profile(user=user)
        profile.save()    

