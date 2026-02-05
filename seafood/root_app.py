
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def home(request):
    return Response({
                    "message": "Welcome to the Seafood API",
                     "status": "API is running smoothly",
                     "URLS": {
                        "users": f"{request.scheme}://{request.get_host()}/api/v1/users/",
                        "roles": f"{request.scheme}://{request.get_host()}/api/v1/roles/",
                        "shipments": f"{request.scheme}://{request.get_host()}/api/v1/shipments/",
                        "logistics-receipts": f"{request.scheme}://{request.get_host()}/api/v1/logisticsreceipts/",
                        "supplier-purchases": f"{request.scheme}://{request.get_host()}/api/v1/supplierpurchases/",
                        "sales": f"{request.scheme}://{request.get_host()}/api/v1/sales/",
                        "cost-ledgers": f"{request.scheme}://{request.get_host()}/api/v1/costledgers/",
                        "currencies": f"{request.scheme}://{request.get_host()}/api/v1/currencies/",
                        "payments": f"{request.scheme}://{request.get_host()}/api/v1/payments/",
                        "exchange-rates": f"{request.scheme}://{request.get_host()}/api/v1/exchange-rates/",
                        "unitofmeasures": f"{request.scheme}://{request.get_host()}/api/v1/unitofmeasures/",
                        "productcategories": f"{request.scheme}://{request.get_host()}/api/v1/productcategories/",
                        "products": f"{request.scheme}://{request.get_host()}/api/v1/products/",

                     },
                     "version": "1.0.0",
                     "documentation_url": "/docs/",
                     })
    