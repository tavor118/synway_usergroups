""" Tests for UserViewSet."""

# pylint: disable=maybe-no-member

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from seed.factories import UserFactory, GroupFactory
from ..models import CustomUser


class UserViewSetTest(APITestCase):
    """ Tests for UserViewSet."""

    def setUp(self):
        self.user = UserFactory()
        self.group = GroupFactory
        self.user_registration_data = {
            'username': 'test_user',
            'password1': 'test_password',
            'password2': 'test_password',
            'group': 1
        }
        self.user_login_data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        self.user_update_data = {
            'username': 'test_user',
            'group': 1
        }

    def test_get_valid_users(self):
        """Test getting valid users."""

        response = self.client.get(
            reverse('customuser-detail', kwargs={'pk': self.user.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        UserFactory.create_batch(2)
        response = self.client.get(reverse('customuser-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_user(self):
        """Test getting invalid users."""

        UserFactory.create_batch(2)
        response = self.client.get(reverse('customuser-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_register_user(self):
        """Test user registration."""

        users_count = CustomUser.objects.count()
        response = self.client.post(
            reverse('rest_register'),
            self.user_registration_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        users_count += 1
        self.assertEqual(CustomUser.objects.count(), users_count)

    def test_update_user_without_permissions(self):
        """Test user updating without permissions."""

        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)
        response = self.client.put(
            reverse('customuser-detail', kwargs={'pk': self.user.pk}),
            self.user_update_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_with_permissions(self):
        """Test user updating with permissions."""

        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.put(
            reverse('customuser-detail', kwargs={'pk': user.pk}),
            self.user_update_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user_without_permissions(self):
        """Test user deleting without permissions."""

        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)
        response = self.client.delete(
            reverse('customuser-detail', kwargs={'pk': self.user.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_with_permissions(self):
        """Test user deleting with permissions."""

        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.delete(
            reverse('customuser-detail', kwargs={'pk': user.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
