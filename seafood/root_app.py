
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def home(request):
    return Response({
                    "message": "Welcome to the Seafood API",
                     "status": "API is running smoothly",
                     "URLS": {
                         "users": "/api/v1/users/",
                         "shipments": "/api/v1/shipments/",
                        "logistics_receipts": "/api/v1/logistics-receipts/",
                         "supplier_purchases": "/api/v1/supplier_purchases/",
                     },
                     "version": "1.0.0",
                     "documentation_url": "/docs/",
                     })
    