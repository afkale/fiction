import os

from django.contrib.auth.models import Group
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from books.models import Book, Page
from fiction.permissions import Groups
from users.models import User


class BookViewSetTests(APITestCase):
    def setUp(self) -> None:
        with open(os.devnull, "w") as devnull:
            call_command("creategroups", stdout=devnull, stderr=devnull)

        self.viewers_group = Group.objects.get(name=Groups.VIEWERS)
        self.editors_group = Group.objects.get(name=Groups.EDITORS)

        self.editor = User.objects.create_user(username="editor", password="editor")
        self.viewer = User.objects.create_user(username="viewer", password="viewer")

        self.editor.groups.add(self.editors_group)
        self.viewer.groups.add(self.viewers_group)

        self.editor_token = f"Bearer {RefreshToken.for_user(self.editor).access_token}"
        self.viewer_token = f"Bearer {RefreshToken.for_user(self.viewer).access_token}"

        Book.objects.create(title="Test book", author="Test author")

        self.url = "/api/books/"

    def test_editor_can_add_book(self) -> None:
        """An editor user should be able to add books."""
        data = {"title": "string", "author": "string"}
        response = self.client.post(
            self.url, data=data, HTTP_AUTHORIZATION=self.editor_token
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_viewer_cannot_add_book(self) -> None:
        """An viewer user should not be able to add books."""
        data = {"title": "string", "author": "string"}
        response = self.client.post(
            self.url, data=data, HTTP_AUTHORIZATION=self.viewer_token
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_edit_book(self) -> None:
        """An editor user should be able to edit books."""
        data = {"title": "string", "author": "string"}
        response = self.client.put(
            f"{self.url}1/", data=data, HTTP_AUTHORIZATION=self.editor_token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], "string")

    def test_viewer_cannot_edit_book(self) -> None:
        """An viewer user should not be able to edit books."""
        data = {"title": "string", "author": "string"}
        response = self.client.put(
            f"{self.url}1/", data=data, HTTP_AUTHORIZATION=self.viewer_token
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_read_books(self) -> None:
        """An editor user should be able to list books."""
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.editor_token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)

    def test_viewer_can_read_books(self) -> None:
        """A viewer user should be able to list books."""
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.viewer_token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)

    def test_editor_can_read_book(self) -> None:
        """An editor user should be able to read a book."""
        response = self.client.get(
            f"{self.url}1/", HTTP_AUTHORIZATION=self.editor_token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_viewer_can_read_book(self) -> None:
        """A viewer user should be able to read a book."""
        response = self.client.get(
            f"{self.url}1/", HTTP_AUTHORIZATION=self.viewer_token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PageViewSetTests(APITestCase):
    def setUp(self) -> None:
        with open(os.devnull, "w") as devnull:
            call_command("creategroups", stdout=devnull, stderr=devnull)

        self.viewers_group = Group.objects.get(name=Groups.VIEWERS)
        self.editors_group = Group.objects.get(name=Groups.EDITORS)

        self.editor = User.objects.create_user(username="editor", password="editor")
        self.viewer = User.objects.create_user(username="viewer", password="viewer")

        self.editor.groups.add(self.editors_group)
        self.viewer.groups.add(self.viewers_group)

        self.editor_token = f"Bearer {RefreshToken.for_user(self.editor).access_token}"
        self.viewer_token = f"Bearer {RefreshToken.for_user(self.viewer).access_token}"

        book = Book.objects.create(title="Test book", author="Test author")
        Page.objects.create(content="Test content", book=book)

        self.url = "/api/pages/"

    def test_editor_can_add_page(self) -> None:
        """An editor user should be able to add pages."""
        data = {"content": "test", "book": 1}
        response = self.client.post(
            self.url, data=data, HTTP_AUTHORIZATION=self.editor_token
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_viewer_cannot_add_page(self) -> None:
        """An viewer user should not be able to add pages."""
        data = {"content": "test", "book": 1}
        response = self.client.post(
            self.url, data=data, HTTP_AUTHORIZATION=self.viewer_token
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_edit_page(self) -> None:
        """An editor user should be able to edit pages."""
        data = {"content": "test", "book": 1}
        response = self.client.put(
            f"{self.url}1/", data=data, HTTP_AUTHORIZATION=self.editor_token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["content"], "test")

    def test_viewer_cannot_edit_page(self) -> None:
        """An viewer user should not be able to edit pages."""
        data = {"content": "test", "book": 1}
        response = self.client.put(
            f"{self.url}1/", data=data, HTTP_AUTHORIZATION=self.viewer_token
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_read_pages(self) -> None:
        """An editor user should be able to list pages."""
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.editor_token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)

    def test_viewer_can_read_pages(self) -> None:
        """A viewer user should be able to list pages."""
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.viewer_token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)

    def test_editor_can_read_page(self) -> None:
        """An editor user should be able to read a page."""
        response = self.client.get(
            f"{self.url}1/", HTTP_AUTHORIZATION=self.editor_token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_viewer_can_read_page(self) -> None:
        """A viewer user should be able to read a page."""
        response = self.client.get(
            f"{self.url}1/", HTTP_AUTHORIZATION=self.viewer_token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
