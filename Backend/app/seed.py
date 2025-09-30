from sqlalchemy.orm import Session
from app.config import SessionLocal, engine
from app.models import Product, Customer, Order, Payment, RepairRequest, Settings
from app.services.customer import CustomerService
from app.schemas import (
    ProductCreate, CustomerCreate, OrderCreate, PaymentCreate, 
    RepairRequestCreate, SettingsCreate
)
import json

def create_seed_data():
    """Create seed data with error handling to prevent startup failures"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Product).first() or db.query(Customer).first():
            print("Seed data already exists, skipping...")
            return
        
        # Create sample products
        products_data = [
            {
                "name": "iPhone 14 Pro",
                "description": "Latest iPhone with Pro camera system",
                "category": "Electronics",
                "sub_category": "Smartphones",
                "brand": "Apple",
                "model": "iPhone 14 Pro",
                "price": 85000.0,
                "original_price": 90000.0,
                "stock": 25,
                "sku": "IPH14PRO001",
                "warranty": "1 year",
                "condition": "new",
                "tags": ["smartphone", "ios", "camera", "5g"],
                "processor": "A16 Bionic",
                "ram": "6GB",
                "storage": "128GB",
                "storage_type": "SSD",
                "screen_size": "6.1 inch",
                "os": "iOS 16",
                "camera": "48MP Pro camera",
                "battery": "3200mAh",
                "color": "Deep Purple",
                "weight": "206g",
                "connectivity": "5G, WiFi 6, Bluetooth 5.3",
                "images": ["https://example.com/iphone14pro.jpg"],
                "status": "active"
            },
            {
                "name": "MacBook Air M2",
                "description": "Lightweight laptop with M2 chip",
                "category": "Computers",
                "sub_category": "Laptops",
                "brand": "Apple",
                "model": "MacBook Air M2",
                "price": 120000.0,
                "stock": 15,
                "sku": "MBA-M2-001",
                "warranty": "1 year",
                "condition": "new",
                "tags": ["laptop", "macbook", "m2", "ultrabook"],
                "processor": "Apple M2",
                "ram": "8GB",
                "storage": "256GB",
                "storage_type": "SSD",
                "screen_size": "13.6 inch",
                "os": "macOS Ventura",
                "battery": "18 hours",
                "color": "Space Gray",
                "weight": "1.24kg",
                "connectivity": "WiFi 6, Bluetooth 5.0, 2x Thunderbolt 4",
                "images": ["https://example.com/macbookair.jpg"],
                "status": "active"
            }
        ]
        
        for product_data in products_data:
            product = Product(**product_data)
            db.add(product)
        
        # Create sample customer with short password to avoid bcrypt issues
        customer_data = CustomerCreate(
            name="John Doe",
            email="john@example.com",
            phone="+254712345678",
            password="pass123"  # Short password to ensure bcrypt compatibility
        )
        customer = CustomerService.create_customer(db, customer_data)
        
        # Commit products and customer
        db.commit()
        
        # Create sample order
        order_data = {
            "customer_id": customer.id,
            "products": [
                {
                    "id": 1,
                    "name": "iPhone 14 Pro",
                    "quantity": 1,
                    "price": 85000.0
                }
            ],
            "total": 85000.0,
            "payment_method": "M-Pesa",
            "shipping_address": {
                "street": "123 Main St",
                "city": "Nairobi",
                "postal_code": "00100",
                "country": "Kenya"
            }
        }
        
        order = Order(**order_data)
        db.add(order)
        db.commit()
        db.refresh(order)
        
        # Create sample payment
        payment_data = {
            "order_id": order.id,
            "method": "M-Pesa",
            "amount": 85000.0,
            "status": "success",
            "transaction_id": "TXN123456789",
            "phone_number": "+254712345678"
        }
        
        payment = Payment(**payment_data)
        db.add(payment)
        
        # Create sample repair request
        repair_data = {
            "customer_name": "Jane Smith",
            "customer_email": "jane@example.com",
            "customer_phone": "+254798765432",
            "device_type": "Smartphone",
            "device_brand": "Samsung",
            "device_model": "Galaxy S22",
            "issue_description": "Screen cracked after dropping",
            "urgency": "normal",
            "estimated_cost": 8000.0,
            "status": "submitted"
        }
        
        repair = RepairRequest(**repair_data)
        db.add(repair)
        
        # Create sample settings
        settings_data = {
            "store_name": "TechHub Kenya",
            "store_description": "Your one-stop shop for electronics and tech repairs",
            "contact_email": "info@techhub.co.ke",
            "contact_phone": "+254700123456",
            "address": {
                "street": "Tom Mboya Street",
                "city": "Nairobi",
                "postal_code": "00100",
                "country": "Kenya"
            },
            "currency": "KES",
            "tax_rate": 0.16,
            "free_shipping_threshold": 10000.0,
            
            # Payment settings
            "payment_mpesa_enabled": True,
            "payment_card_enabled": True,
            "payment_cod_enabled": True,
            "payment_mpesa_shortcode": "174379",
            "payment_mpesa_passkey": "test_passkey_123",
            "payment_mpesa_consumer_key": "test_consumer_key",
            "payment_mpesa_consumer_secret": "test_consumer_secret",
            
            # Shipping settings
            "shipping_standard_fee": 200.0,
            "shipping_express_fee": 500.0,
            "shipping_free_enabled": True,
            "shipping_same_day_enabled": False,
            
            # Notification settings
            "notifications_email_enabled": True,
            "notifications_sms_enabled": True,
            "notifications_order_confirmations": True,
            "notifications_low_stock_alerts": True,
            "notifications_new_order_alerts": True
        }
        
        settings = Settings(**settings_data)
        db.add(settings)
        
        db.commit()
        print("Seed data created successfully!")
        
    except Exception as e:
        print(f"Warning: Error creating seed data: {e}")
        print("Application will continue without seed data...")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_seed_data()