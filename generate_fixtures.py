import json
import uuid
from datetime import datetime, timedelta
import random

# Generate UUIDs for consistent references
def gen_uuid():
    return str(uuid.uuid4())

# Base date for timestamps
base_date = datetime(2026, 1, 1, 10, 0, 0)

fixtures = []

# 1. Roles
# Define roles map for easy lookup
role_ids = {
    "Admin": "02915c14-1092-4733-ae0a-f3067a27b67e",
    "Mozambique Agent": gen_uuid(),
    "Logistics Agent": gen_uuid(),
    "Sales Agent": gen_uuid(),
    "Finance Agent": gen_uuid(),
    "Viewer": gen_uuid()
}

for role_name, role_id in role_ids.items():
    fixtures.append({
        "model": "users.role",
        "pk": role_id,
        "fields": {"role_name": role_name, "permissions": []}
    })

# 2. Users
# (Name, Location, Email, Role)
user_configs = [
    ("Admin User", "Headquarters", "admin@seafood.com", "Admin"),
    ("Mozambique Agent", "Maputo", "mozambique@seafood.com", "Mozambique Agent"),
    ("Logistics Agent", "Nairobi", "logistics@seafood.com", "Logistics Agent"),
    ("Sales Agent", "Headquarters", "sales@seafood.com", "Sales Agent"),
    ("Finance Agent", "Headquarters", "finance@seafood.com", "Finance Agent"),
    ("Viewer Partner", "Remote", "viewer@seafood.com", "Viewer"),
    ("Operations Manager", "Nairobi", "ops@seafood.com", "Admin"),
    ("Procurement Officer", "Mombasa", "procurement@seafood.com", "Mozambique Agent"), # Test multiple users in same role
    ("Warehouse Supervisor", "Mombasa", "warehouse@seafood.com", "Logistics Agent"),
    ("Accounts Manager", "Headquarters", "accounts@seafood.com", "Finance Agent"),
]

user_ids = []
for i, (name, location, email, role_name) in enumerate(user_configs):
    user_id = "2ce1134f-d2a4-4bac-a0f6-bffe82743cea" if i == 0 else gen_uuid()
    user_ids.append(user_id)
    fixtures.append({
        "model": "users.user",
        "pk": user_id,
        "fields": {
            "password": "pbkdf2_sha256$870000$VqZJhN8zKxQ8YqZJhN8zKx$8zKxQ8YqZJhN8zKxQ8YqZJhN8zKxQ8YqZJhN8zKxQ8Y=",
            "last_login": None,
            "is_superuser": role_name == "Admin",
            "email": email,
            "role_id": role_ids[role_name],
            "full_name": name,
            "location": location,
            "is_active": True,
            "is_staff": role_name == "Admin",
            "created_at": (base_date + timedelta(days=i)).isoformat() + "Z",
            "updated_at": (base_date + timedelta(days=i)).isoformat() + "Z",
            "groups": [],
            "user_permissions": []
        }
    })

# 3. Currencies (10 items - replaced EUR with MZN)
currencies_data = [
    ("USD", "US Dollar", "$"),
    ("KES", "Kenyan Shilling", "KSh"),
    ("TZS", "Tanzanian Shilling", "TSh"),
    ("MZN", "Mozambique Metical", "MT"),
    ("CNY", "Chinese Yuan (Renminbi)", "¥"),
    ("GBP", "British Pound", "£"),
    ("JPY", "Japanese Yen", "¥"),
    ("AED", "UAE Dirham", "د.إ"),
    ("SAR", "Saudi Riyal", "﷼"),
    ("UGX", "Ugandan Shilling", "USh"),
]

currency_ids = {}
for code, name, symbol in currencies_data:
    curr_id = gen_uuid()
    currency_ids[code] = curr_id
    fixtures.append({
        "model": "currencies.currency",
        "pk": curr_id,
        "fields": {
            "code": code,
            "name": name,
            "symbol": symbol,
            "is_active": True,
            "created_at": base_date.isoformat() + "Z"
        }
    })

# 4. Exchange Rates - Updated to match user's data
# Primary rates to KSH (from user's image)
exchange_pairs = [
    ("TZS", "KES", 0.0501461648),
    ("MZN", "KES", 2.040500443),
    ("CNY", "KES", 18.7291117),
    ("USD", "KES", 130.094298),
    # Additional useful pairs
    ("GBP", "KES", 165.00),
    ("JPY", "KES", 0.88),
    ("AED", "KES", 35.40),
    ("SAR", "KES", 34.70),
    ("UGX", "KES", 0.035),
    # Reverse pairs for conversions
    ("USD", "GBP", 0.79),
    ("USD", "JPY", 148.50),
    ("USD", "CNY", 7.25),
    ("USD", "TZS", 2350.00),
]

for from_code, to_code, rate in exchange_pairs:
    fixtures.append({
        "model": "exchangerates.exchangerate",
        "pk": gen_uuid(),
        "fields": {
            "from_currency_id": currency_ids[from_code],
            "to_currency_id": currency_ids[to_code],
            "rate": str(rate),
            "rate_date": (base_date + timedelta(days=random.randint(0, 30))).date().isoformat(),
            "created_at": base_date.isoformat() + "Z"
        }
    })

# 5. Product Categories (10 items)
categories = ["Fresh Fish", "Frozen Fish", "Shellfish", "Crustaceans", "Mollusks", "Cephalopods", "Processed Seafood", "Smoked Fish", "Dried Fish", "Canned Seafood"]
category_ids = {}
for cat in categories:
    cat_id = gen_uuid()
    category_ids[cat] = cat_id
    fixtures.append({
        "model": "productcategories.productcategory",
        "pk": cat_id,
        "fields": {
            "name": cat,
            "created_at": base_date.isoformat() + "Z"
        }
    })

# 6. Units of Measure (10 items)
units = [
    ("kg", "Kilograms"),
    ("pcs", "Pieces"),
    ("ctn", "Cartons"),
    ("lbs", "Pounds"),
    ("ton", "Metric Tons"),
    ("box", "Boxes"),
    ("bag", "Bags"),
    ("crate", "Crates"),
    ("pallet", "Pallets"),
    ("dozen", "Dozens"),
]

unit_ids = {}
for code, desc in units:
    unit_id = gen_uuid()
    unit_ids[code] = unit_id
    fixtures.append({
        "model": "unitofmeasures.unitofmeasure",
        "pk": unit_id,
        "fields": {
            "code": code,
            "description": desc,
            "created_at": base_date.isoformat() + "Z"
        }
    })

# 7. Products (15 items)
products_data = [
    ("Nile Perch Fillet", "Fresh Fish", "kg", "Premium quality Nile Perch fillets"),
    ("Tilapia Whole", "Fresh Fish", "kg", "Fresh whole tilapia"),
    ("Tuna Steaks", "Frozen Fish", "kg", "Frozen yellowfin tuna steaks"),
    ("King Prawns", "Crustaceans", "kg", "Large king prawns"),
    ("Lobster Tails", "Crustaceans", "pcs", "Premium lobster tails"),
    ("Octopus", "Cephalopods", "kg", "Fresh octopus"),
    ("Squid Rings", "Cephalopods", "kg", "Cleaned squid rings"),
    ("Oysters", "Mollusks", "dozen", "Fresh oysters"),
    ("Mussels", "Mollusks", "kg", "Fresh mussels"),
    ("Smoked Salmon", "Smoked Fish", "kg", "Premium smoked salmon"),
    ("Dried Anchovies", "Dried Fish", "kg", "Sun-dried anchovies"),
    ("Canned Tuna", "Canned Seafood", "ctn", "Canned tuna in oil"),
    ("Crab Meat", "Crustaceans", "kg", "Fresh crab meat"),
    ("Mackerel Frozen", "Frozen Fish", "kg", "Frozen mackerel"),
    ("Sardines Fresh", "Fresh Fish", "kg", "Fresh sardines"),
]

product_ids = []
for name, cat, unit, desc in products_data:
    prod_id = gen_uuid()
    product_ids.append(prod_id)
    fixtures.append({
        "model": "products.product",
        "pk": prod_id,
        "fields": {
            "name": name,
            "category_id": category_ids[cat],
            "unit_id": unit_ids[unit],
            "description": desc,
            "is_active": True,
            "created_at": base_date.isoformat() + "Z"
        }
    })

# 8. Shipments (12 items)
shipment_ids = []
origins = ["Kenya", "Tanzania", "Uganda", "Somalia", "Seychelles", "Mauritius"]
statuses = ["CREATED", "IN_TRANSIT", "RECEIVED", "COMPLETED"]

for i in range(12):
    ship_id = gen_uuid()
    shipment_ids.append(ship_id)
    fixtures.append({
        "model": "shipments.shipment",
        "pk": ship_id,
        "fields": {
            "currency_id": currency_ids["USD"],
            "created_at": (base_date + timedelta(days=i*3)).isoformat() + "Z",
            "country_origin": origins[i % len(origins)],
            "status": statuses[min(i // 3, 3)]
        }
    })

# 9. Shipment Items (20 items - multiple items per shipment)
for i in range(20):
    fixtures.append({
        "model": "shipments.shipmentitem",
        "fields": {
            "shipment_id": shipment_ids[i % 12],
            "product_id": product_ids[i % 15],
            "quantity": random.randint(50, 500),
            "price_at_shipping": str(round(random.uniform(5.0, 50.0), 2))
        }
    })

# 10. Supplier Purchases (12 items)
for i in range(12):
    fixtures.append({
        "model": "supplierpurchases.supplierpurchase",
        "pk": gen_uuid(),
        "fields": {
            "shipment_id": shipment_ids[i],
            "currency_id": currency_ids["USD"],
            "entered_by_id": user_ids[i % len(user_ids)],
            "kg_purchased": str(round(random.uniform(100.0, 1000.0), 2)),
            "image_urls": "",
            "created_at": (base_date + timedelta(days=i*3, hours=2)).isoformat() + "Z"
        }
    })

# 11. Logistics Receipts (12 items)
facilities = ["Freezer 01 - Nairobi", "Freezer 02 - Mombasa", "Cold Storage A - Nairobi", "Warehouse B - Mombasa"]

for i in range(12):
    net_kg = round(random.uniform(80.0, 950.0), 2)
    fixtures.append({
        "model": "logisticsreceipts.logisticsreceipt",
        "pk": gen_uuid(),
        "fields": {
            "shipment_id": shipment_ids[i],
            "entered_by_id": user_ids[i % len(user_ids)],
            "net_received_kg": str(net_kg),
            "transport_loss_kg": str(round(random.uniform(1.0, 10.0), 2)),
            "freezing_loss_kg": str(round(random.uniform(0.5, 5.0), 2)),
            "facility_location": facilities[i % 4],
            "notes": f"Receipt #{i+1} processed successfully",
            "created_at": (base_date + timedelta(days=i*3, hours=4)).isoformat() + "Z"
        }
    })

# 12. Sales (12 items)
sale_ids = []
for i in range(12):
    sale_id = gen_uuid()
    sale_ids.append(sale_id)
    qty = round(random.uniform(50.0, 800.0), 2)
    price = round(random.uniform(10.0, 50.0), 2)
    total = round(qty * price, 2)
    fixtures.append({
        "model": "sales.sale",
        "pk": sale_id,
        "fields": {
            "shipment_id": shipment_ids[i],
            "currency_id": currency_ids["USD"],
            "entered_by_id": user_ids[i % len(user_ids)],
            "kg_sold": str(qty),
            "quantity_sold": str(qty),
            "selling_price": str(price),
            "exchange_rate_used": None,
            "converted_amount": str(total),
            "total_sale_amount": str(total),
            "created_at": (base_date + timedelta(days=i*3+1, hours=1)).isoformat() + "Z"
        }
    })

# 13. Payments (15 items)
for i in range(15):
    sale_idx = i % 12
    fixtures.append({
        "model": "payments.payment",
        "pk": gen_uuid(),
        "fields": {
            "sale_id": sale_ids[sale_idx],
            "entered_by_id": user_ids[i % len(user_ids)],
            "currency_id": currency_ids["USD"],
            "buyer_name": f"Buyer Company {chr(65+sale_idx)}",
            "amount_paid": str(round(random.uniform(100.0, 10000.0), 2)),
            "expected_payment_date": (base_date + timedelta(days=i*2+7)).date().isoformat(),
            "actual_payment_date": (base_date + timedelta(days=i*2+8)).date().isoformat() if i % 3 != 0 else None,
            "created_at": (base_date + timedelta(days=i*2+1)).isoformat() + "Z"
        }
    })

# 14. Cost Ledgers (15 items)
cost_categories = ["Transport", "Freezing", "Cold Storage", "Packing Materials", "Labor", "Commissions", "Export Fees", "Fuel"]

for i in range(15):
    fixtures.append({
        "model": "costledgers.costledger",
        "pk": gen_uuid(),
        "fields": {
            "shipment_id": shipment_ids[i % 12],
            "entered_by_id": user_ids[i % len(user_ids)],
            "cost_category": cost_categories[i % len(cost_categories)],
            "amount": str(round(random.uniform(50.0, 5000.0), 2)),
            "other_category": None,
            "currency_id": currency_ids["USD"],
            "created_at": (base_date + timedelta(days=i*2)).isoformat() + "Z",
            "exchange_rate_used": None,
            "converted_amount": str(round(random.uniform(50.0, 5000.0), 2))
        }
    })

# Write to file
with open('/home/khalifah/Desktop/SeaFood/data.json', 'w') as f:
    json.dump(fixtures, f, indent=2)

print(f"Generated {len(fixtures)} fixture records successfully!")
print("Breakdown:")
print(f"  - Roles: {len(role_ids)}")
print(f"  - Users: {len(user_configs)}")
print(f"  - Currencies: {len(currencies_data)}")
print(f"  - Exchange Rates: {len(exchange_pairs)}")
print(f"  - Product Categories: {len(categories)}")
print(f"  - Units of Measure: {len(units)}")
print(f"  - Products: {len(products_data)}")
print(f"  - Shipments: 12")
print(f"  - Shipment Items: 20")
print(f"  - Supplier Purchases: 12")
print(f"  - Logistics Receipts: 12")
print(f"  - Sales: 12")
print(f"  - Payments: 15")
print(f"  - Cost Ledgers: 15")
