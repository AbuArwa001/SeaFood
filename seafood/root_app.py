
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
                        "logistics_receipts": f"{request.scheme}://{request.get_host()}/api/v1/logistics-receipts/",
                        "supplier_purchases": f"{request.scheme}://{request.get_host()}/api/v1/supplier_purchases/",
                        "sales": f"{request.scheme}://{request.get_host()}/api/v1/sales/",
                        "cost_ledgers": f"{request.scheme}://{request.get_host()}/api/v1/cost_ledgers/",
                        "currencies": f"{request.scheme}://{request.get_host()}/api/v1/currencies/",
                        "payments": f"{request.scheme}://{request.get_host()}/api/v1/payments/",
                        "exchange_rates": f"{request.scheme}://{request.get_host()}/api/v1/exchange-rates/",
                        "unit_of_measures": f"{request.scheme}://{request.get_host()}/api/v1/unit-of-measures/",
                        "product_categories": f"{request.scheme}://{request.get_host()}/api/v1/productcategories/",
                        "products": f"{request.scheme}://{request.get_host()}/api/v1/products/",

                     },
                     "version": "1.0.0",
                     "documentation_url": "/docs/",
                     })
    