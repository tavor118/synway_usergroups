"""Serializer for groups applications."""

from rest_framework import serializers
from .models import Group


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for Group Model.
    """
    users = serializers.HyperlinkedRelatedField(
        many=True, view_name='customuser-detail', read_only=True
    )

    class Meta:
        model = Group
        fields = ('url', 'id', 'name', 'description',
                  'users', 'created', 'modified')
