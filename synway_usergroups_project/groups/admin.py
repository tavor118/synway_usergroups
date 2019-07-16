"""Module for interaction with an admin interface."""

from django.contrib import admin
from .models import Group

admin.site.register(Group)
