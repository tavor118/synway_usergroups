"""Serializers for users application."""

from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user."""

    class Meta:
        model = models.CustomUser
        fields = ('url', 'id', 'username', 'created', 'group')
