from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from utils.models import AbstractUUID, AbstractTimeTracker
from accounts.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractUUID, AbstractTimeTracker):
    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='First Name'
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Last Name'
    )
    phone = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Phone Number'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )
    iin = models.CharField(
        max_length=12,
        unique=True,
        verbose_name='IIN'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='is_active'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='is_staff'
    )
    is_superuser = models.BooleanField(
        default=True,
        verbose_name='is_superuser'
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'iin']

    object = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-updated_at', '-created_at']
