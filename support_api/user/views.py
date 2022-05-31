from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAdminUser
from user.models import User
from user.serializer import UserSerializer
from rest_framework import viewsets, mixins


class RegisterAPIView(mixins.CreateModelMixin,
                      GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
