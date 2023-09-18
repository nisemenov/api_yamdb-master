from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(raw_password=password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None,
                         **extra_fields):
        extra_fields.setdefault('role', 'admin')
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    bio = models.CharField(max_length=250, blank=True)
    email = models.EmailField(
        error_messages={
            'unique': 'A user with that email already exists.',
        },
        unique=True
    )

    objects = UserManager()

    ROLE = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('user', 'User')
    ]

    role = models.CharField(
        max_length=9,
        choices=ROLE,
        default='user'
    )

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
