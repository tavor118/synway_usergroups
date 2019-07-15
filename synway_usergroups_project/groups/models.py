"""Models for groups application."""

from django.db import models
from django_extensions.db.models import TimeStampedModel


class Group(TimeStampedModel, models.Model):
    """Model for blogs."""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()


    def __str__(self):
        return self.name

    class Meta:
        ordering = ["created"]
