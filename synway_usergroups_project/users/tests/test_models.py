""" Tests for User model."""

from django.test import TestCase

from seed.factories import UserFactory
from users.models import CustomUser


class UserModelTest(TestCase):
    """ Tests for CustomUser model."""

    def setUp(self):
        self.user = UserFactory(username="test_user", email="test_user@example.com")

    def test_user_creation(self):
        """Test CustomUser Model creation."""
        self.assertEqual(self.user.username, "test_user")
        self.assertEqual(self.user.email, "test_user@example.com")
        users_count = CustomUser.objects.count()
        UserFactory.create_batch(2)
        users_count += 2
        self.assertEqual(CustomUser.objects.count(), users_count)

    def test_user_str(self):
        """Test for string representation."""
        self.assertEqual(str(self.user), "test_user")
