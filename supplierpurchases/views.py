from rest_framework import permissions, viewsets
from supplierpurchases.models import SupplierPurchase
from .serializers import SupplierPurchaseSerializer
from django.conf import settings
import boto3
import uuid
import datetime
from botocore.exceptions import NoCredentialsError

from users.permissions import IsMozambiqueAgent, IsOwnerOrAdmin

class SupplierPurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierPurchaseSerializer
    permission_classes = [permissions.IsAuthenticated, IsMozambiqueAgent, IsOwnerOrAdmin]
    search_fields = ['id', 'shipment__id']

    def get_queryset(self):
        user = self.request.user
        if user.role.role_name == "Admin":
            return SupplierPurchase.objects.all()
        return SupplierPurchase.objects.filter(entered_by=user)

    def perform_create(self, serializer):
        image_files = self.request.FILES.getlist('image_files')
        image_urls = serializer.validated_data.get('image_urls', []) or []

        if image_files:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            
            shipment_id = serializer.validated_data.get('shipment').id
            date_str = datetime.datetime.now().strftime('%Y-%m-%d')
            
            for index, image_file in enumerate(image_files):
                file_extension = image_file.name.split('.')[-1]
                object_name = f"purchases/{date_str}/{shipment_id}_{index}.{file_extension}"

                try:
                    s3_client.upload_fileobj(
                        image_file,
                        settings.AWS_STORAGE_BUCKET_NAME,
                        object_name,
                        ExtraArgs={'ContentType': image_file.content_type}
                    )
                    image_urls.append(f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{object_name}")
                except NoCredentialsError:
                    pass

        serializer.save(entered_by=self.request.user, image_urls=image_urls)
