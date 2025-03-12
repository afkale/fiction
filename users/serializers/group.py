from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer[Group]):
    """Serializer for the Group model."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Config for Group model serializer."""

        model = Group
        fields = ["id", "name"]  #

