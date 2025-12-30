# 📦 Shipment & Sales Management Backend

A comprehensive Django-based backend system for managing shipments, supplier purchases, logistics receipts, sales, payments, and cost tracking. This system is engineered for enhanced traceability, financial accountability, and role-based data entry using UUID identifiers as primary keys.

## 🚀 Features

- ✅ **UUID-based Primary Keys** - Secure and scalable identifier system
- 👥 **Role-Based User Structure** - Granular access control for different user types
- 📦 **Shipment Lifecycle Tracking** - Complete visibility from creation to completion
- 🧾 **Supplier Purchase Recording** - Documented procurement management
- 🚚 **Logistics Receipt & Loss Tracking** - Accurate inventory and loss monitoring
- 💰 **Sales & Payment Management** - Comprehensive sales order and payment processing
- 📊 **Cost Ledger** - Detailed profitability analysis and cost tracking
- 🔐 **Audit Trail** - Built-in accountability through explicit entered_by fields
- 🧱 **Normalized Schema** - Clean, well-structured relational database design

## 🏗️ Technology Stack

| Component | Technology |
|-----------|----------|
| **Backend Framework** | [![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/) |
| **Database** | [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/) |
| **ORM** | [![Django ORM](https://img.shields.io/badge/Django%20ORM-092E20?style=for-the-badge&logo=django&logoColor=white)](https://docs.djangoproject.com/en/stable/topics/db/models/) |
| **Identifiers** | UUID (Universal Unique Identifiers) |
| **Architecture** | Modular, domain-driven

## 📂 Project Structure

```
project/
├── app/
│   ├── models.py
│   ├── admin.py
│   ├── apps.py
│   └── migrations/
├── manage.py
└── README.md
```

## 🧩 Domain Models Overview

### 👥 Roles & Users

- **Role** - Defines system roles (Admin, Accountant, Logistics, etc.)
- **User** - System users linked to roles

### 📦 Shipment

Represents a complete shipment lifecycle with the following attributes:

- Product information
- Currency specification
- Origin country
- Status tracking (Created, In Transit, Received, Completed)

### 🧾 Supplier Purchases

Tracks supplier purchases with the following details:

- Weight purchased (kg)
- Proof images
- User entry audit trail

### 🚚 Logistics Receipts

Monitors logistics operations and loss tracking:

- Net received weight
- Transport loss
- Freezing loss
- Facility location

### 💰 Sales

Manages sales operations per shipment:

- Quantity sold
- Selling price
- Currency conversion
- Total sale value

### 💳 Payments

Tracks buyer payment information:

- Expected vs. actual payment dates
- Partial or full payment tracking

### 📊 Cost Ledger

Tracks operational costs:

- Cost categories (Transport, Storage, Tax, etc.)
- Amount per shipment

## 🔗 Entity Relationships

```
Role → User
User → SupplierPurchase
User → LogisticsReceipt
User → Sale
User → Payment
User → CostLedger

Shipment → SupplierPurchase
Shipment → LogisticsReceipt
Shipment → Sale
Shipment → CostLedger

Sale → Payment
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/your-repo.git
cd your-repo
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install django psycopg2-binary
```

### 4. Configure Environment

Update the database configuration in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shipment_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Start Development Server

```bash
python manage.py runserver
```

## 🔐 Data Integrity & Design Decisions

- **UUID Prevention** - UUIDs prevent ID enumeration attacks and provide scalability
- **Foreign Key Protection** - `PROTECT` constraints used for critical audit fields (entered_by)
- **Cascade Behavior** - `CASCADE` constraints applied where child records depend on parent records
- **Financial Data Handling** - `DecimalField` used for all financial and weight data to ensure precision
- **Audit Design** - Explicit `entered_by` fields enable comprehensive audit trails

## 📈 Recommended Extensions

The following enhancements are recommended for production deployments:

- Django REST Framework for comprehensive API layer
- Role-based permission system (django-guardian or custom)
- Shipment profit & loss reports
- Stock balance calculations
- Currency conversion service integration
- Soft deletes and activity logs

## 🧪 Testing

Run the test suite using Django's testing framework:

```bash
python manage.py test
```

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 👨‍💻 Author

**Khalfani Khalfan**  
Backend Engineer | DevOps | Systems Design  
Kenya 🇰🇪