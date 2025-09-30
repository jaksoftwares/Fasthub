from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from app.config import Base

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String(255), default="My E-Commerce Store")
    store_description = Column(String(500))
    contact_email = Column(String(255))
    contact_phone = Column(String(20))
    address = Column(JSON)  # Store address as JSON
    currency = Column(String(10), default="KES")
    tax_rate = Column(Float, default=0.16)  # 16% VAT for Kenya
    free_shipping_threshold = Column(Float, default=1000.0)
    
    # Payment settings
    payment_mpesa_enabled = Column(Boolean, default=True)
    payment_card_enabled = Column(Boolean, default=True)
    payment_cod_enabled = Column(Boolean, default=True)
    payment_mpesa_shortcode = Column(String(20))
    payment_mpesa_passkey = Column(String(255))
    payment_mpesa_consumer_key = Column(String(255))
    payment_mpesa_consumer_secret = Column(String(255))
    
    # Shipping settings
    shipping_standard_fee = Column(Float, default=200.0)
    shipping_express_fee = Column(Float, default=500.0)
    shipping_free_enabled = Column(Boolean, default=True)
    shipping_same_day_enabled = Column(Boolean, default=False)
    
    # Notification settings
    notifications_email_enabled = Column(Boolean, default=True)
    notifications_sms_enabled = Column(Boolean, default=True)
    notifications_order_confirmations = Column(Boolean, default=True)
    notifications_low_stock_alerts = Column(Boolean, default=True)
    notifications_new_order_alerts = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Settings(id={self.id}, store_name='{self.store_name}')>"