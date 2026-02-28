from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import SystemParameter
from .serializers import SystemParameterSerializer
from users.permissions import IsAdmin
from rest_framework_simplejwt.authentication import JWTAuthentication

class SystemParameterViewSet(viewsets.ModelViewSet):
    queryset = SystemParameter.objects.all()
    serializer_class = SystemParameterSerializer
    authentication_classes = [JWTAuthentication]
    lookup_field = 'key'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Non-admins can read parameters if they are authenticated
            return [permissions.IsAuthenticated()]
        return [IsAdmin()]

    def list(self, request, *args, **kwargs):
        # Filter public parameters for non-admins
        if not IsAdmin().has_permission(request, self):
            self.queryset = self.queryset.filter(is_public=True)
        
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not IsAdmin().has_permission(request, self) and not instance.is_public:
            return Response(
                {"detail": "You do not have permission to access this parameter."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
