Create a complete FastAPI backend for a single-store e-commerce application with full support for analytics dashboards.

Requirements:
1. Project structure:
   - app/main.py (entry point)
   - app/config.py (database settings with SQLAlchemy + SQLite for Replit free tier)
   - app/models/ (SQLAlchemy models: products, customers, orders, repairs, settings)
   - app/schemas/ (Pydantic schemas)
   - app/routes/ (API endpoints per entity: products, customers, orders, repairs, settings, analytics)
   - app/services/ (business logic per domain)
   - app/seed.py (insert example seed data)

2. Entities and fields:

Product:
- id, name, description, category, subCategory, brand, model,
  price, originalPrice?, stock, sku, warranty, condition, tags [string[]],
  processor?, ram?, storage?, storageType?, graphics?, screenSize?, os?,
  camera?, battery?, color?, weight?, dimensions?, connectivity?, additionalSpecs?,
  images [string[]], status, createdAt.

Customer:
- id, name, email, password (hashed with passlib), phone,
  totalOrders, totalSpent, status, joinDate, lastOrder.

Order:
- id, customer, email, products [array of product items with id, name, quantity, price],
  total, status, paymentMethod, date, shippingAddress.

RepairRequest:
- id, customerName, customerEmail, customerPhone,
  deviceType, deviceBrand, deviceModel, issueDescription, urgency,
  estimatedCost, status, submittedAt, updatedAt, notes, technicianNotes.

Settings:
- storeName, storeDescription, contactEmail, contactPhone, address,
  currency, taxRate, freeShippingThreshold,
  payment (mpesaEnabled, cardPaymentsEnabled, codEnabled, mpesaShortcode, mpesaPasskey),
  shipping (standardShippingFee, expressShippingFee, freeShippingEnabled, sameDayDeliveryEnabled),
  notifications (emailNotifications, smsNotifications, orderConfirmations, lowStockAlerts, newOrderAlerts).

3. Features:
- Products: CRUD APIs.
- Customers: CRUD APIs (passwords hashed).
- Orders: Create order, list orders, get order details.
- Repair requests: Create, update status, list.
- Settings: CRUD APIs for store, payment, shipping, notifications.
- Analytics: Provide data for dashboards:
   a. /analytics/sales-trend → monthly sales + order counts
   b. /analytics/categories → sales by category (for PieChart)
   c. /analytics/top-products → top 5 selling products with units + revenue
   d. /analytics/stats → KPIs (total revenue, total orders, total customers, total products)
   e. /analytics/customer-metrics → avg rating (mocked), satisfaction (mocked), avg delivery time (mocked)
   f. /analytics/orders-trend → order counts by month (for line chart)

4. Database:
- SQLite for development (Replit-friendly).
- SQLAlchemy ORM models.
- Alembic migrations optional; use Base.metadata.create_all fallback.

5. APIs:
- Each entity has its own router in app/routes/.
- Return JSON responses.
- Auto Swagger docs at /docs.

6. Extras:
- requirements.txt with: fastapi, uvicorn, sqlalchemy, pydantic, alembic, passlib[bcrypt].
- Seed data for: at least 2 products, 1 customer, 1 order, 1 repair request, 1 settings record, plus some fake analytics data.
- Startup event should auto-create tables and insert seed data if empty.

7. Deployment:
- Must run with: uvicorn app.main:app --host=0.0.0.0 --port=8000
- Ensure it runs on Replit free tier (no external DB).

Generate all necessary files and working code in one shot.
