from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets

from books.models import Book, Page
from books.serializers.book import BookSerializer
from books.serializers.page import PageSerializer


class BookViewSet(viewsets.ModelViewSet[Book]):
    queryset = Book.objects.all().order_by("-created")
    serializer_class = BookSerializer
    permission_classes = [DjangoModelPermissions]


class PageViewSet(viewsets.ModelViewSet[Page]):
    queryset = Page.objects.all().order_by("-created")
    serializer_class = PageSerializer
    permission_classes = [DjangoModelPermissions]
