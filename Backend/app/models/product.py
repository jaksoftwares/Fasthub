from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from app.config import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, index=True)
    description = Column(Text)
    category = Column(String(100), nullable=False, index=True)
    sub_category = Column(String(100))
    brand = Column(String(100))
    model = Column(String(100))
    price = Column(Float, nullable=False)
    original_price = Column(Float)
    stock = Column(Integer, default=0)
    sku = Column(String(100), unique=True, index=True)
    warranty = Column(String(100))
    condition = Column(String(50), default="new")
    tags = Column(JSON)  # Array of strings stored as JSON
    
    # Tech specs (optional fields)
    processor = Column(String(100))
    ram = Column(String(50))
    storage = Column(String(50))
    storage_type = Column(String(50))
    graphics = Column(String(100))
    screen_size = Column(String(50))
    os = Column(String(100))
    camera = Column(String(100))
    battery = Column(String(50))
    color = Column(String(50))
    weight = Column(String(50))
    dimensions = Column(String(100))
    connectivity = Column(String(100))
    additional_specs = Column(JSON)  # Additional specifications as JSON
    
    images = Column(JSON)  # Array of image URLs stored as JSON
    status = Column(String(20), default="active")  # active, inactive, discontinued
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', slug='{self.slug}', price={self.price})>"