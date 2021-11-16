from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django_countries.fields import CountryField    #country 사용 + pip install django-countries
from typing import Optional

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, nickname, country, password=None):
        if not email:
            raise ValueError('Sorry, ALL BLAZE USERS must have an EMAIL address :-)')

        user = self.model(
            email = self.normalize_email(email),
            nickname = nickname,   
            country = country,
        )

        user.is_admin = False
        user.is_superuser = False
        user.is_staff = False
        user.is_active = True

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, nickname, password, country):
        user = self.create_user(   
            email = self.normalize_email(email),
            nickname = nickname,
            country=country,
            password = password,
            
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        
        user.save(using=self._db)
        return user

        #'BlazeUser'
class BlazeUser(AbstractBaseUser,PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(
        verbose_name='email',
        max_length=100,
        null=False,
        unique=True,
    )
    nickname = models.CharField(
        verbose_name='nickname',
        max_length = 10,
        null=False,
        unique=True,
    )
    country = CountryField()

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname','country']

    class Meta:
        verbose_name = ("user")
        verbose_name_plural = ("users")

        def __Str__(self):
            return self.email
