from django.shortcuts import render
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from users.permissions import CanCreateUser, IsAdmin
from .models import User, Role
from .serializers import UserSerializer, RoleSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.action == 'me':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), CanCreateUser()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Return the current authenticated user's profile.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='change_password')
    def change_password(self, request):
        """
        Allow an authenticated user to change their own password.
        POST /api/v1/users/change_password/
        Body: { current_password, new_password, confirm_password }
        """
        user = request.user
        current_password = request.data.get('current_password', '')
        new_password = request.data.get('new_password', '')
        confirm_password = request.data.get('confirm_password', '')

        if not current_password or not new_password or not confirm_password:
            return Response(
                {'detail': 'current_password, new_password and confirm_password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(current_password):
            return Response(
                {'detail': 'Current password is incorrect.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password != confirm_password:
            return Response(
                {'detail': 'New passwords do not match.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({'detail': ' '.join(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save(update_fields=['password'])
        return Response({'detail': 'Password updated successfully.'}, status=status.HTTP_200_OK)

class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = None
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdmin]