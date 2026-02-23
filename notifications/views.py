from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from shipments.models import Shipment
from payments.models import Payment


class NotificationsView(APIView):
    """
    GET /api/v1/notifications/
    Returns a derived list of actionable notifications based on current data state.
    No database model — all alerts are computed at query time.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
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
                "type": "payment_overdue",
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
                    "type": "shipment_late",
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

        # Sort: critical first, then warning, then info
        severity_order = {"critical": 0, "warning": 1, "info": 2}
        notifications.sort(key=lambda n: severity_order.get(n["severity"], 3))

        return Response({
            "count": len(notifications),
            "results": notifications,
        })
