from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    products = Column(JSON, nullable=False)  # Array of product items with id, name, quantity, price
    total = Column(Float, nullable=False)
    status = Column(String(20), default="pending")  # pending, paid, shipped, completed, cancelled
    payment_method = Column(String(50))
    date = Column(DateTime(timezone=True), server_default=func.now())
    shipping_address = Column(JSON)  # Address details as JSON

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    payments = relationship("Payment", back_populates="order")

    def __repr__(self):
        return f"<Order(id={self.id}, customer_id={self.customer_id}, total={self.total}, status='{self.status}')>"

# Add relationship to Customer model
from app.models.customer import Customer
Customer.orders = relationship("Order", back_populates="customer")