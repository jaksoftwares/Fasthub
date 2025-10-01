# Save as app/scripts/unseed.py
from app.config import SessionLocal
from app.models import Product, Customer, Order, Payment, RepairRequest, Settings

db = SessionLocal()
db.query(Payment).delete()
db.query(Order).delete()
db.query(Product).delete()
db.query(Customer).delete()
db.query(RepairRequest).delete()
db.query(Settings).delete()
db.commit()
db.close()
print("All data deleted.")