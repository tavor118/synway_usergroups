""" Tests for GroupViewSet."""

# pylint: disable=maybe-no-member

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..models import Group
from seed.factories import (UserFactory,
                            GroupFactory)


class GroupViewSetTest(APITestCase):
    """ Tests for GroupViewSet."""

    def setUp(self):
        self.group = GroupFactory()
        self.user = UserFactory(group=self.group)
        self.group_data = {
            'name': 'Hello World!',
            'description': 'Hello World Everyone!'
        }

    def test_get_valid_groups(self):
        """Test getting valid groups."""

        GroupFactory.create_batch(2)
        response = self.client.get(reverse('group-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('group-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_group(self):
        """Test getting invalid groups."""

        GroupFactory.create_batch(2)
        response = self.client.get(reverse('group-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_group_without_authentication(self):
        """Test group creating without authentications."""

        response = self.client.post(reverse('group-list'), self.group_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_valid_group(self):
        """Test valid group creating."""

        # forcibly authenticate a request
        self.client.force_authenticate(user=self.user)
        # make an authenticated request to the view
        response = self.client.post(reverse('group-list'), self.group_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_group(self):
        """Test invalid group creating ."""

        # forcibly authenticate a request
        self.client.force_authenticate(user=self.user)
        # make an authenticated request to the view...
        response = self.client.post(reverse('group-list'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_group_without_authentication(self):
        """Test valid group creating without authentication."""

        group = self.group
        response = self.client.put(
            reverse('group-detail', kwargs={'pk': group.pk}), self.group_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_valid_group(self):
        """Test valid group updating."""

        user = self.user
        group = GroupFactory()
        # forcibly authenticate a request
        self.client.force_authenticate(user=user)
        # make an authenticated request to the view...
        response = self.client.put(
            reverse('group-detail', kwargs={'pk': group.pk}), self.group_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_group(self):
        """Test invalid group updating."""

        user = self.user
        GroupFactory()
        # forcibly authenticate a request
        self.client.force_authenticate(user=user)
        # make an authenticated request to the view...
        response = self.client.put(
            reverse('group-detail', kwargs={'pk': 999}), self.group_data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_valid_group_with_invalid_data(self):
        """Test group updating with invalid data."""

        user = self.user
        group = GroupFactory()
        # forcibly authenticate a request
        self.client.force_authenticate(user=user)
        # make an authenticated request to the view...
        response = self.client.put(
            reverse('group-detail', kwargs={'pk': group.pk}), {}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_group_without_authentication(self):
        """Test group deleting without authentication."""

        group = self.group
        response = self.client.delete(
            reverse('group-detail', kwargs={'pk': group.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_group_with_users(self):
        """Test group deleting with users."""

        user = self.user
        group_id = self.group.id
        # forcibly authenticate a request
        self.client.force_authenticate(user=user)
        # make an authenticated request to the view
        response = self.client.delete(
            reverse('group-detail', kwargs={'pk': self.group.pk}), self.group_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(type(response.data[0]), ErrorDetail)
        self.assertEqual(str(response.data[0]), "Can't delete group with users.")

    def test_delete_group_without_users(self):
        """Test group deleting without users."""

        group = GroupFactory()
        user = self.user
        group_id = group.id
        # forcibly authenticate a request
        self.client.force_authenticate(user=user)
        group_count = Group.objects.count()
        # make an authenticated request to the view
        response = self.client.delete(
            reverse('group-detail', kwargs={'pk': group.pk}), self.group_data
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            group = None
        self.assertIsNone(group)
        group_count -= 1
        self.assertEqual(Group.objects.count(), group_count)

