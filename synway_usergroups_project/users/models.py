"""Models for users application."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.models import TimeStampedModel

from groups.models import Group


class CustomUser(TimeStampedModel, AbstractUser):
    """Custom User model."""
    group = models.ForeignKey(
        Group, related_name='users', on_delete=models.PROTECT,
        blank=True, null=True
    )

    def __str__(self):
        return self.username
