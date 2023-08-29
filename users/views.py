from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from users.models import User
from users.serializers import UserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
