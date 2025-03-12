from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserViewSetTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", password="admin", email="admin@example.com"
        )
        self.user = User.objects.create_user(
            username="user", password="user", email="user@example.com"
        )
        self.admin_token = RefreshToken.for_user(self.admin).access_token
        self.user_token = RefreshToken.for_user(self.user).access_token

        self.url = "/api/users/"

    def test_admin_can_list_users(self):
        """Un administrador puede listar todos los usuarios"""
        self.client.login(username="admin", password="admin")
        response = self.client.get(
            self.url, HTTP_AUTHORIZATION=f"Bearer {self.admin_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 2)

    def test_non_admin_cannot_list_users(self):
        """Un usuario normal no puede acceder a la lista de usuarios"""
        self.client.login(username="user", password="user")
        response = self.client.get(
            self.url, HTTP_AUTHORIZATION=f"Bearer {self.user_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_user(self):
        """Un administrador puede crear un nuevo usuario"""
        self.client.login(username="admin", password="admin")
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com",
        }
        response = self.client.post(
            self.url, data=data, HTTP_AUTHORIZATION=f"Bearer {self.user_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_non_admin_cannot_create_user(self):
        """Un usuario normal no puede crear un nuevo usuario"""
        self.client.login(username="user", password="user")
        data = {"username": "baduser", "password": "password"}
        response = self.client.post(
            self.url, data=data, HTTP_AUTHORIZATION=f"Bearer {self.user_token}"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_user(self):
        """Un administrador puede eliminar un usuario"""
        self.client.login(username="admin", password="admin")
        response = self.client.delete(
            f"{self.url}{self.user.id}/",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

    def test_non_admin_cannot_delete_user(self):
        """Un usuario normal no puede eliminar a otro usuario"""
        self.client.login(username="user", password="user")
        response = self.client.delete(
            f"{self.url}{self.admin.id}/",
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
