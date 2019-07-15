""" Tests for CustomUser serializer."""

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from seed import factories

from ..serializers import UserSerializer


class UserSerializerTest(TestCase):
    """ Tests for CustomUser serializer."""

    def setUp(self):
        self.group = factories.GroupFactory()
        self.user = factories.UserFactory(group = self.group)

    def test_model_fields(self):
        """Test if serializer data matches the CustomUser object fields."""

        request = APIRequestFactory().get({})
        serializer = UserSerializer(
            self.user, context={'request': request}
        )

        self.assertEqual(
            serializer.data['group'], self.group.id
        )

        for field_name in ('id', 'username'):
            self.assertEqual(
                serializer.data[field_name],
                getattr(self.user, field_name)
            )
