from rest_framework import serializers

from books.models import Book, Page


class _BookPageSerializer(serializers.ModelSerializer[Page]):
    """Book page general serializer."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Book page serializer meta configuration."""

        model = Page
        fields = ["id", "content", "created", "modified"]


class BookSerializer(serializers.ModelSerializer[Book]):
    """Book general serializer."""

    pages = _BookPageSerializer(many=True, read_only=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """Book serializer meta configuration."""

        model = Book
        fields = ["id", "title", "author", "pages", "created", "modified"]
