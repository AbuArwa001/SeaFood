# Improved Knock Workflow Templates

These templates are optimized for readability, visual impact, and full use of the data provided by the backend.

### 💰 Payment Completed (`payment_completed`)
**Template:**
"New Payment: **{{ buyer_name }}** just paid **{{ amount }}** for Invoice #{{ invoice_id }}. Total MRR updated."

---

### ⚠️ Payment Overdue (`payment_overdue`)
**Template:**
"Overdue Alert: **{{ buyer_name }}**'s account is now **{{ days_overdue }} days** past due. Amount pending: {{ amount_due }}."

---

### 🚀 Sale Created (`sale_created`)
**Template:**
"🚀 **New Sale Alert!**

**Actor**: {{ actor_name }}
**Customer**: {{ buyer_name }}
**Total**: {{ total_price }}
**Weight**: {{ kg_sold }} kg

**Items**: {{ items_list }}

[Approve Fulfillment]"

---

### 📦 Shipment Received (`shipment_received`)
**Template:**
"📦 **Shipment Received**

Order **#{{ order_id }}** was successfully delivered and processed by **{{ actor_name }}** at **{{ facility_location }}**.

**Net Received**: {{ net_received_kg }} kg.
No further action required."
