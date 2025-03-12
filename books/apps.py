from django.apps import AppConfig


class BooksConfig(AppConfig):
    """Book app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "books"
