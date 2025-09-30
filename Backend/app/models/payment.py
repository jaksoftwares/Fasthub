from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    method = Column(String(50), nullable=False)  # M-Pesa, Card, COD
    amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending")  # pending, success, failed
    transaction_id = Column(String(255), unique=True, index=True)
    phone_number = Column(String(20))  # For M-Pesa payments
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    order = relationship("Order", back_populates="payments")

    def __repr__(self):
        return f"<Payment(id={self.id}, order_id={self.order_id}, method='{self.method}', amount={self.amount}, status='{self.status}')>"