from random import randint
import os
from uuid import uuid4

from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings


def user_avatar_file_path(instance, filename):
    ext = str(filename).split('.')[-1]
    filename = f'{uuid4()}.{ext}'
    return os.path.join('users-avatars/', filename)



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^(998)\d{9}$', message="998901234567 holatda kiriting")
    phone_number = models.CharField(_('Telefon raqami'), max_length=16, validators=[phone_regex],
                                    unique=True, help_text=_('998901234567 holatda kiriting'))
    USERNAME_FIELD = 'phone_number'

    # additional fields
    firstname = models.CharField(
        _('Ismi:'), max_length=150, null=True, blank=True)
    lastname = models.CharField(
        _('Familyasi:'), max_length=150, null=True, blank=True)
    avatar = models.FileField(upload_to=user_avatar_file_path, null=True, blank=True)

    # set AbstractUser defaults
    date_joined = models.DateTimeField(
        _('Ro‘yxatdan o‘tgan sanasi'), default=timezone.now)
    is_superuser = models.BooleanField(
        _('Administratormi?'),
        default=False,
        help_text=_('Administrator huquqini beradi'),
    )
    is_staff = models.BooleanField(
        _('Moderatormi?'),
        default=False,
        help_text=_('Admin qismiga kirish huquqini beradi.'),
    )
    is_active = models.BooleanField(
        _('Aktivmi?'),
        default=True,
        help_text=_('Saytga kirish huquqini beradi.'),
    )
    objects = UserManager()

    class Meta:
        verbose_name = _('Foydalanuvchi')
        verbose_name_plural = _('Foydalanuvchilar')

    def full_name(self):
        if self.firstname and self.lastname:
            return self.firstname + ' ' + self.lastname
        elif self.firstname:
            return self.firstname
        elif self.lastname:
            return self.lastname
        else:
            return ""

    def __str__(self):
        return self.full_name()


def _generate_verification_code():
    range_start = 10 ** (6 - 1)
    range_end = (10 ** 6) - 1
    return randint(range_start, range_end)


def _expire_at_default():
    return timezone.now() + timezone.timedelta(minutes=settings.CODE_VERIFICATION_EXPIRE_TIME)


class VerificationCode(models.Model):
    code_regex = RegexValidator(regex=r'^\d{6}$',
                                message="123456 holatda kiriting")
    code = models.CharField(_('Maxfiy kod'), max_length=6, validators=[
        code_regex], default=_generate_verification_code)
    contact = models.CharField(_('Aloqa raqami'), max_length=255,
                               null=False, blank=False)
    expire_at = models.DateTimeField(_('Yaroqlilik muddati'),
                                     default=_expire_at_default)

    def __str__(self):
        return str(self.contact)
