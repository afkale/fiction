from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserViewSetTests(APITestCase):
    def setUp(self) -> None:
        self.admin = User.objects.create_superuser(
            username="admin", password="admin", email="admin@example.com"
        )
        self.user = User.objects.create_user(
            username="user", password="user", email="user@example.com"
        )
        self.admin_token = RefreshToken.for_user(self.admin).access_token
        self.user_token = RefreshToken.for_user(self.user).access_token

        self.url = "/api/users/"

    def test_admin_can_list_users(self) -> None:
        """An admin user should be able to list users."""
        response = self.client.get(
            self.url, HTTP_AUTHORIZATION=f"Bearer {self.admin_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 2)

    def test_non_admin_cannot_list_users(self) -> None:
        """A non admin user should not be able to list user."""
        response = self.client.get(
            self.url, HTTP_AUTHORIZATION=f"Bearer {self.user_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_user(self) -> None:
        """An admin user should be able to create users."""
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com",
        }
        response = self.client.post(
            self.url, data=data, HTTP_AUTHORIZATION=f"Bearer {self.admin_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_non_admin_cannot_create_user(self) -> None:
        """A non admin user should not be able to create user."""
        data = {"username": "baduser", "password": "password"}
        response = self.client.post(
            self.url, data=data, HTTP_AUTHORIZATION=f"Bearer {self.user_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_user(self) -> None:
        """An admin user should be able to delete users."""
        response = self.client.delete(
            f"{self.url}{self.user.id}/",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

    def test_non_admin_cannot_delete_user(self) -> None:
        """A non admin user should not be able to delete user."""
        response = self.client.delete(
            f"{self.url}{self.admin.id}/",
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GroupViewSetTests(APITestCase):
    def setUp(self) -> None:
        self.admin = User.objects.create_superuser(
            username="admin", password="admin", email="admin@example.com"
        )
        self.user = User.objects.create_user(
            username="user", password="user", email="user@example.com"
        )

        Group.objects.create(name="Group1")
        Group.objects.create(name="Group2")

        self.admin_token = RefreshToken.for_user(self.admin).access_token
        self.user_token = RefreshToken.for_user(self.user).access_token

        self.url = "/api/groups/"

    def test_admin_can_list_groups(self) -> None:
        """An admin user should be able to list groups."""
        response = self.client.get(
            self.url, HTTP_AUTHORIZATION=f"Bearer {self.admin_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 2)

    def test_non_admin_cannot_list_groups(self) -> None:
        """A non admin user should not be able to list groups."""
        response = self.client.get(
            self.url, HTTP_AUTHORIZATION=f"Bearer {self.user_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_group(self) -> None:
        """An admin user should be able to create a group."""
        data = {"name": "newgroup"}
        response = self.client.post(
            self.url, data=data, HTTP_AUTHORIZATION=f"Bearer {self.admin_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_non_admin_cannot_create_group(self) -> None:
        """A non admin user should not be able to create groups."""
        data = {"name": "newgroup"}
        response = self.client.post(
            self.url, data=data, HTTP_AUTHORIZATION=f"Bearer {self.user_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_group(self) -> None:
        """An admin user should be able to delete groups."""
        response = self.client.delete(
            f"{self.url}1/", HTTP_AUTHORIZATION=f"Bearer {self.admin_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Group.objects.count(), 1)

    def test_non_admin_cannot_delete_group(self) -> None:
        """A non admin user should not be able to delete groups."""
        response = self.client.delete(
            f"{self.url}1/",
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
