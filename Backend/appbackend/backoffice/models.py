from asyncio.windows_events import NULL
from multiprocessing.sharedctypes import Value
import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from backoffice.models import UserManager
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'),unique=True, db_index=True)
    First_name = models.CharField(_("first name"), max_length=50, blank=True) #what the fuck does blank=True mean
    Last_name = models.CharField(_("last name"), max_length=50, blank=True)
    googleId = models.CharField() #needed if signing in with google email
    android = models.BooleanField(blank=True, default=False) #need to update to modern django
    ios = models.BooleanField(blank=True, default=False, null=True) #need to update to modern django
    is_valid = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='/avatars', null=True, blank=True)
    lastConnexionDate = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    @property
    def last_login(self):
        return self.lastConnexionDate

    def __str__(self):
        return u'%s' % (self.email)

class UserManage(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a user with the given email and password
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True.')
        return self._create_user(email, password, **extra_fields)

class Expense(models.Model):
    def tempshit(self):
        return "im dumb"

class Expense_list(models.Model):
    def tempshit(self):
        return "im dumb"
