from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions

from books.models import Book, Page
from books.serializers import BookSerializer, PageSerializer


class BookViewSet(viewsets.ModelViewSet[Book]):
    """CRUD book model viewset."""

    queryset = Book.objects.all().order_by("-created")  # pylint: disable=no-member
    serializer_class = BookSerializer
    permission_classes = [DjangoModelPermissions]


class PageViewSet(viewsets.ModelViewSet[Page]):
    """CRUD page model viewset."""

    queryset = Page.objects.all().order_by("-created")  # pylint: disable=no-member
    serializer_class = PageSerializer
    permission_classes = [DjangoModelPermissions]
