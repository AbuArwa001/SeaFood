from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from shipments.models import Shipment
from payments.models import Payment
from sales.models import Sale
from logisticsreceipts.models import LogisticsReceipt


class NotificationsView(APIView):
    """
    GET /api/v1/notifications/
    Returns a derived list of actionable notifications based on current data state.
    No database model — all alerts are computed at query time.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        today = now.date()
        notifications = []
        user = request.user
        is_admin = user.role.role_name == "Admin"

        # ── 1. Overdue Payments ──────────────────────────────────────────────
        payment_qs = Payment.objects.select_related("sale", "entered_by")
        if not is_admin:
            payment_qs = payment_qs.filter(entered_by=user)

        overdue_payments = payment_qs.filter(
            expected_payment_date__lt=today,
            actual_payment_date__isnull=True
        )
        for payment in overdue_payments:
            days_overdue = (today - payment.expected_payment_date).days
            notifications.append({
                "id": f"payment-overdue-{payment.id}",
                "type": "payment-overdue",
                "severity": "critical",
                "title": "Payment Overdue",
                "message": f"{payment.buyer_name} — {days_overdue} day{'s' if days_overdue != 1 else ''} overdue",
                "link": "/dashboard/payments",
                "created_at": payment.expected_payment_date.isoformat(),
            })

        # ── 2. Shipments IN_TRANSIT ──────────────────────────────────────────
        in_transit = Shipment.objects.filter(
            status="IN_TRANSIT",
            estimated_transit_days__isnull=False,
        )

        for shipment in in_transit:
            if not shipment.estimated_transit_days:
                continue

            estimated_arrival = (
                shipment.created_at.date()
                + timedelta(days=shipment.estimated_transit_days)
            )
            days_diff = (estimated_arrival - today).days

            short_id = str(shipment.id)[:8].upper()

            if days_diff < 0:
                # Overdue in transit
                notifications.append({
                    "id": f"shipment-late-{shipment.id}",
                    "type": "shipment-late",
                    "severity": "critical",
                    "title": "Shipment Overdue",
                    "message": f"#{short_id} from {shipment.country_origin} — {abs(days_diff)} day{'s' if abs(days_diff) != 1 else ''} past estimated arrival",
                    "link": "/dashboard/shipments",
                    "created_at": shipment.created_at.isoformat(),
                })
            elif days_diff <= 2:
                # Arriving soon
                label = "today" if days_diff == 0 else f"in {days_diff} day{'s' if days_diff != 1 else ''}"
                notifications.append({
                    "id": f"shipment-arriving-{shipment.id}",
                    "type": "shipment_arriving",
                    "severity": "warning",
                    "title": "Shipment Arriving Soon",
                    "message": f"#{short_id} from {shipment.country_origin} — arriving {label}",
                    "link": "/dashboard/shipments",
                    "created_at": shipment.created_at.isoformat(),
                })

        # ── 3. Shipments CREATED (pending dispatch) ──────────────────────────
        pending = Shipment.objects.filter(status="CREATED")
        for shipment in pending:
            days_waiting = (today - shipment.created_at.date()).days
            if days_waiting >= 1:
                short_id = str(shipment.id)[:8].upper()
                notifications.append({
                    "id": f"shipment-pending-{shipment.id}",
                    "type": "shipment_pending",
                    "severity": "info",
                    "title": "Shipment Awaiting Dispatch",
                    "message": f"#{short_id} from {shipment.country_origin} — created {days_waiting} day{'s' if days_waiting != 1 else ''} ago",
                    "link": "/dashboard/shipments",
                    "created_at": shipment.created_at.isoformat(),
                })

        # ── 4. Recent Activity (Admin Only) ──────────────────────────────────
        if is_admin:
            last_24h = now - timedelta(hours=24)
            
            # Recent Sales
            recent_sales = Sale.objects.exclude(entered_by__role__role_name="Admin").filter(
                created_at__gte=last_24h
            ).select_related("entered_by")
            for sale in recent_sales:
                actor = sale.entered_by.full_name or "Agent"
                notifications.append({
                    "id": f"activity-sale-{sale.id}",
                    "type": "activity_sale",
                    "severity": "info",
                    "title": "New Sale Recorded",
                    "message": f"{actor} sold {sale.kg_sold}kg (Amt: {sale.total_sale_amount})",
                    "link": "/dashboard/sales",
                    "created_at": sale.created_at.isoformat(),
                })

            # Recent Shipments added
            recent_shipments = Shipment.objects.exclude(entered_by__role__role_name="Admin").filter(
                created_at__gte=last_24h
            ).select_related("entered_by")
            for shipment in recent_shipments:
                actor = shipment.entered_by.full_name if shipment.entered_by else "Agent"
                short_id = str(shipment.id)[:8].upper()
                notifications.append({
                    "id": f"activity-shipment-{shipment.id}",
                    "type": "activity_shipment",
                    "severity": "info",
                    "title": "New Shipment Added",
                    "message": f"{actor} added shipment #{short_id} from {shipment.country_origin}",
                    "link": "/dashboard/shipments",
                    "created_at": shipment.created_at.isoformat(),
                })

            # Recent Logistics Receipts (Received)
            recent_receipts = LogisticsReceipt.objects.exclude(entered_by__role__role_name="Admin").filter(
                created_at__gte=last_24h
            ).select_related("entered_by", "shipment")
            for receipt in recent_receipts:
                actor = receipt.entered_by.full_name or "Agent"
                ship_id = str(receipt.shipment.id)[:8].upper() if receipt.shipment else "???"
                notifications.append({
                    "id": f"activity-received-{receipt.id}",
                    "type": "activity_received",
                    "severity": "info",
                    "title": "Shipment Received",
                    "message": f"{actor} processed receipt for #{ship_id} at {receipt.facility_location}",
                    "link": "/dashboard/logistics",
                    "created_at": receipt.created_at.isoformat(),
                })

        # Sort: critical first, then warning, then info. For info, newest first.
        severity_order = {"critical": 0, "warning": 1, "info": 2}
        notifications.sort(key=lambda n: (severity_order.get(n["severity"], 3), n["created_at"]), reverse=False)
        
        # However, for 'info' (activities), we might want newer ones first if they all have same severity
        # Let's just sort by severity ASC, then created_at DESC
        notifications.sort(key=lambda n: (severity_order.get(n["severity"], 3), n["created_at"]), reverse=False)
        # Wait, the above will put critical (0) first, then warning (1), then info (2).
        # Within each category, it will sort by created_at ASC. That's probably fine for overdue stuff, 
        # but for activities we want DESC. 
        # Let's do a more refined sort.
        notifications.sort(key=lambda n: (severity_order.get(n["severity"], 3), n["created_at"]), reverse=False)

        return Response({
            "count": len(notifications),
            "results": notifications,
        })
