import os
import sys
import django
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

# Setup Django environment
sys.path.append('/home/khalfan/Desktop/SeaFood')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seafood.settings')
django.setup()

from users.models import User, Role
from shipments.models import Shipment, ShipmentItem
from products.models import Product
from currencies.models import Currency
from sales.models import Sale
from payments.models import Payment
from logisticsreceipts.models import LogisticsReceipt

def generate_data():
    print("--- Starting Test Data Generation ---")

    # 1. Get or Create necessary baseline entities
    admin_role, _ = Role.objects.get_or_create(role_name="Admin")
    agent_role, _ = Role.objects.get_or_create(role_name="Sales Agent")
    logistics_role, _ = Role.objects.get_or_create(role_name="Logistics Agent")

    # Get an Agent user (to perform actions)
    agent_user = User.objects.filter(role=agent_role).first()
    if not agent_user:
        agent_user = User.objects.create_user(
            email="test_agent@seafood.com",
            full_name="Test Agent",
            location="Mombasa",
            role=agent_role,
            password="password123",
            first_name="Test",
            middle_name="Agent",
            last_name="One",
            phone_number="1234567890",
            is_email_verified=True
        )
    
    # Get a Logistics user
    logistics_user = User.objects.filter(role=logistics_role).first()
    if not logistics_user:
        logistics_user = User.objects.create_user(
            email="test_logistics@seafood.com",
            full_name="Test Logistics",
            location="Nairobi",
            role=logistics_role,
            password="password123",
            first_name="Test",
            middle_name="Logistics",
            last_name="One",
            phone_number="0987654321",
            is_email_verified=True
        )

    # Get a Currency
    currency = Currency.objects.filter(code="USD").first()
    if not currency:
        currency = Currency.objects.create(code="USD", name="US Dollar", symbol="$")

    # Get a Product
    product = Product.objects.all().first()
    if not product:
        # Need to handle ProductCategory and UnitOfMeasure if missing
        from productcategories.models import ProductCategory
        from unitofmeasures.models import UnitOfMeasure
        cat, _ = ProductCategory.objects.get_or_create(name="Fish")
        unit, _ = UnitOfMeasure.objects.get_or_create(code="kg", description="Kilogram")
        product = Product.objects.create(name="Fresh Salmon", category=cat, unit=unit, description="Premium Salmon")

    # Get or Create a Shipment
    shipment = Shipment.objects.filter(status="CREATED").first()
    if not shipment:
        shipment = Shipment.objects.create(
            currency=currency,
            country_origin="Norway",
            status="CREATED",
            estimated_transit_days=5
        )
        # Add an item to the shipment
        ShipmentItem.objects.create(
            shipment=shipment,
            product=product,
            quantity=100,
            price_at_shipping=Decimal("15.50")
        )

    print(f"Using Agent: {agent_user.email}")
    print(f"Using Shipment: {shipment.id}")

    # --- NEW: IDENTIFY ALL USERS IN KNOCK ---
    # This ensures both actors (agents) and recipients (admins) exist in Knock.
    from notifications.knock_client import client, trigger_notification
    from notifications.knock_recipients import get_role_recipients

    print("\nSynchronizing users with Knock (Identifying profiles)...")
    all_users = User.objects.filter(is_active=True).select_related('role')
    for u in all_users:
        try:
            client.users.update(
                user_id=str(u.id),
                name=u.full_name,
                email=u.email,
                phone_number=u.phone_number or ""
            )
        except Exception as e:
            print(f"Failed to identify user {u.email}: {e}")
    print("User synchronization complete.")

    # --- TRIGGER 1: Sale Created ---
    print("\nTriggering 'sale_created'...")
    sale1 = Sale.objects.create(
        shipment=shipment,
        entered_by=agent_user,
        currency=currency,
        kg_sold=Decimal("10.5"),
        quantity_sold=Decimal("10.5"),
        selling_price=Decimal("25.00"),
        total_sale_amount=Decimal("262.50"),
        converted_amount=Decimal("262.50")
    )
    
    # Construct items list
    shipment_items = shipment.items.select_related('product').all()
    items_list = ", ".join([f"{item.product.name} ({item.quantity})" for item in shipment_items])

    trigger_notification(
        workflow_key="sale_created",
        recipients=get_role_recipients(),
        actor=str(agent_user.id),
        data={
            "total_price": f"262.50 USD",
            "items_list": items_list,
            "buyer_name": "Test Customer A",
            "kg_sold": "10.5",
            "actor_name": agent_user.full_name,
        }
    )
    print(f"Created Sale and triggered 'sale_created' notification.")

    # --- TRIGGER 2: Payment Completed ---
    print("\nTriggering 'payment_completed'...")
    payment1 = Payment.objects.create(
        sale=sale1,
        entered_by=agent_user,
        currency=currency,
        buyer_name="Atlantic Seafood Co.",
        amount_paid=Decimal("262.50"),
        expected_payment_date=timezone.now().date() + timedelta(days=7),
        actual_payment_date=timezone.now()
    )
    
    trigger_notification(
        workflow_key="payment_completed",
        recipients=get_role_recipients(),
        actor=str(agent_user.id),
        data={
            "amount": "262.50 USD",
            "invoice_id": str(payment1.id)[:8].upper(),
            "buyer_name": payment1.buyer_name,
        }
    )
    print(f"Created Payment and triggered 'payment_completed' notification.")

    # --- TRIGGER 3: Shipment Received ---
    print("\nTriggering 'shipment_received'...")
    receipt1 = LogisticsReceipt.objects.create(
        shipment=shipment,
        entered_by=logistics_user,
        net_received_kg=Decimal("98.5"),
        transport_loss_kg=Decimal("1.5"),
        freezing_loss_kg=Decimal("0.0"),
        facility_location="Mombasa Cold Storage",
        notes="Shipment arrived in good condition"
    )

    trigger_notification(
        workflow_key="shipment_received",
        recipients=get_role_recipients(),
        actor=str(logistics_user.id),
        data={
            "order_id": str(shipment.id)[:8].upper(),
            "actor_name": logistics_user.full_name,
            "facility_location": "Mombasa Cold Storage",
            "net_received_kg": "98.5",
        }
    )
    print(f"Created Receipt and triggered 'shipment_received' notification.")

    # --- TRIGGER 4: Payment Overdue ---
    print("\nPreparing 'payment_overdue' trigger...")
    overdue_payment = Payment.objects.create(
        sale=sale1,
        entered_by=agent_user,
        currency=currency,
        buyer_name="Delayed Foods Ltd",
        amount_paid=Decimal("110.00"),
        expected_payment_date=timezone.now().date() - timedelta(days=5)
    )
    print(f"Created Overdue Payment: {overdue_payment.id} (Expected Date: {overdue_payment.expected_payment_date})")

    print("\n--- Data Generation Complete ---")
    print("To trigger the 'payment_overdue' alert, run:")
    print("python3 manage.py trigger_overdue_notifications")

if __name__ == "__main__":
    generate_data()
