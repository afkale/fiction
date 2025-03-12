# mypy: disable-error-code=var-annotated
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Book(TimeStampedModel):
    """Book model."""

    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)


class Page(TimeStampedModel):
    """Book page model."""

    content = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="pages")
