from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        blank=True,
    )
    role = models.CharField(
        max_length=15,
        choices=[
            ('user', 'user'),
            ('moderator', 'moderator'),
            ('admin', 'admin')
        ],
        default='user',
        blank=True,
    )

    class Meta:
        ordering = (id,)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
