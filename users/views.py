from django.contrib.auth.models import Group
from rest_framework import permissions, viewsets

from users.serializers import GroupSerializer

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet[User]):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet[Group]):
    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]
