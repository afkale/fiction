from rest_framework import serializers

from books.models import Page


class PageSerializer(serializers.ModelSerializer[Page]):
    """Book general serializer."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Book serializer meta configuration."""

        model = Page
        fields = ["id", "content", "book", "created", "modified"]
