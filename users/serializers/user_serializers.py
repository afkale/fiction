from typing import Any, Dict

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    """User general serializer."""

    password = serializers.CharField(write_only=True, required=False)

    class Meta:  # pylint: disable=too-few-public-methods
        """User serializer meta configuration."""

        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_superuser",
            "is_staff",
            "groups",
        ]

    def create(self, validated_data: Dict[str, Any]) -> User:
        """Create user with hashed password"""
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance: User, validated_data: Dict[str, Any]) -> User:
        """Securely update user information, hashing password if provided"""
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
