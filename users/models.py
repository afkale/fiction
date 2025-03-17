from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    This allows for future customization of the user model,
    such as adding additional fields or modifying authentication behavior.
    """
