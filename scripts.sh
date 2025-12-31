for app in users shipments supplierpurchases logisticsreceipts sales costledgers currencies payments exchangerates unitofmeasures productcategories products; do
  mkdir -p $app/migrations
  touch $app/migrations/__init__.py
done
