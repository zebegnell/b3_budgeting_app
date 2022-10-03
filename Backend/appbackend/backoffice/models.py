from asyncio.windows_events import NULL
from email.policy import default
from multiprocessing.sharedctypes import Value
from tabnanny import verbose
import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from backoffice.models import UserManager
from django.contrib.auth.models import BaseUserManager
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'),unique=True, db_index=True)
    First_name = models.CharField(_("first name"), max_length=50, blank=True) #what the fuck does blank=True mean
    Last_name = models.CharField(_("last name"), max_length=50, blank=True)
    googleToken = models.CharField(max_length=200, null=True, blank=True)
    connection_choice = ((0,'ios'), (1,'android'),(2,'browser'))
    connectionType = models.IntegerField(choices=connection_choice, null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='/avatars', null=True, blank=True)
    lastConnexionDate = models.DateTimeField(null=True, blank=True)
    user_budget = models.IntegerField()

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

class UserManager(BaseUserManager):
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

class Expense(models.Model): #actual expense that user inputs
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name=_('name'))
    price = models.FloatField(default=0, verbose_name=_('price'))
    purchaseTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % (self.name)
    
    def pricenum(self):
        return self.price
    
    def expense_name(self):
        return self.name
    
    class Meta:
        verbose_name = ('Expense')
        verbose_name_plural = ('Expenses')

#class Category (models.Model): #Expense categories available to user, can be added to. may not need this. may need to readjust expense and user blocks
#    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#    name = models.CharField(max_length=100, verbose_name=_('name'))
#    
#    class Meta:
#        verbose_name=_('Category')
#        verbose_name_plural=_('Categories')
#
#    def idString(self):
#        return str(self.id)
#
#    def __str__(self):
#        return self.name


class Expense_list(models.Model): #list of all of user's expenses
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    refUser = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    totalExpenses = models.FloatField(default=0, verbose_name=_('totalExpenses'))

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def save(self, *args, **kwargs):
        super(Expense_list, self).save(*args,**kwargs)
