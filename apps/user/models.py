import base64, os
from django.utils.html import mark_safe
from django.utils.html import format_html
from django.db import models

from django.core import validators
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from apps.common_utiles import constants

class UserManager(BaseUserManager):
    def create_user(self,email, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
      
        user.email = email
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email=None, password=None):
        try:
            if not email:
                raise ValueError("User must have an email")
            if not password:
                raise ValueError("User must have a password")

            user = self.model(
                email=self.normalize_email(email)
            )
            user.email = email
            user.set_password(password)
            user.is_superuser = True
            user.save(using=self._db)
            return user
        except BaseException as err:
            print(err)


class User(AbstractBaseUser, PermissionsMixin):

    """all users"""

    first_name = models.CharField(
        'first name',
        max_length=30,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        'last name',
        max_length=30,
        null=True,
        blank=True,
    )

    email = models.CharField(
        'email address',
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        validators=[
            validators.RegexValidator(
                r'^[а-яА-Яa-zA-Z0-9_.+-]+@[а-яА-Яa-zA-Z0-9-]+\.[а-яА-Яa-zA-Z0-9-.]+$',
                'Enter a valid email address.'
            ),
        ]
    )
  
    password = models.CharField(
        'user password',
        max_length=255,
        blank=False,
        null=False,
        default='',
    )

    status = models.CharField(
        choices=constants.STATUS_CHOICES, 
        default='active', 
        max_length=10
    )

    @property
    def is_staff(self):
        ''' IS the user a member of staff? '''
        return (self.status and self.status == 'active')
  
    USERNAME_FIELD = 'email'
    objects = UserManager()



class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=6)
    country = models.CharField(max_length=50)

    def __str__(self):

        return f"({self.city},{self.state},{self.zipcode},{self.country})"

class Hobbies(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):

    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    phone = models.CharField(
        max_length= 15,
        null=True,
        blank= True,
    )
    image = models.ImageField(upload_to ='uploads/',null=True)

    address = models.ManyToManyField(Address,blank=True)
    hobbies = models.ManyToManyField(Hobbies,blank=True)


    def __str__(self):
        if self.user.first_name is not None:
            return self.user.first_name
        return self.user.email


    

