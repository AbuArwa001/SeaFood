from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from users.permissions import CanCreateUser, IsAdminUser
from .models import User, Role
from .serializers import UserSerializer, RoleSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [CanCreateUser] 

class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    authentication_classes = [JWTAuthentication]