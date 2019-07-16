"""Serializers for users application."""

from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user."""

    group = serializers.HyperlinkedRelatedField(view_name='group-detail', read_only=True)
    group_name = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = models.CustomUser
        fields = ('url', 'id', 'username', 'password', 'group', 'group_name')

        extra_kwargs = {
            'password': {'write_only': True},
        }
