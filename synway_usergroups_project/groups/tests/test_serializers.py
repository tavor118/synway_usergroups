""" Tests for Group serializer."""

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from seed.factories import GroupFactory

from ..serializers import GroupSerializer


class GroupSerializerTest(TestCase):
    """ Tests for Group serializer."""

    def setUp(self):
        self.group = GroupFactory()

    def test_model_fields(self):
        """Test if serializer data matches the Group object fields."""

        request = APIRequestFactory().get({})
        serializer = GroupSerializer(self.group, context={'request': request})
        self.assertEqual(
            serializer.data['created'],
            # output datetime in ISO-8601 format
            self.group.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        )
        self.assertEqual(
            serializer.data['modified'],
            self.group.modified.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        )

        for field_name in ('id', 'name', 'description'):
            self.assertEqual(
                serializer.data[field_name],
                getattr(self.group, field_name)
            )
