""" Tests for Group model."""

from django.test import TestCase

from ..models import Group
from seed.factories import (UserFactory,
                            GroupFactory)


class GroupModelTest(TestCase):
    """ Tests for Group model."""

    def setUp(self):
        self.user = UserFactory()
        self.group = GroupFactory()

    def test_groups_creation(self):
        """Test Post Model creation."""
        groups_count = Group.objects.count()
        group_instance = GroupFactory(
            name="Test Title",
            description="Test Description",
        )
        self.assertEqual(group_instance.name, "Test Title")
        self.assertEqual(group_instance.description, "Test Description")
        users = UserFactory.create_batch(2, group=self.group)
        for user in users:
            self.assertEqual(
                user.group.name, self.group.name)
        groups_count += 1
        self.assertEqual(Group.objects.count(), groups_count)

    def test_group_str(self):
        """Test for string representation."""
        self.assertEqual(str(self.group), self.group.name)
