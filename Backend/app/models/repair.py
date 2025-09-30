from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from app.config import Base

class RepairRequest(Base):
    __tablename__ = "repair_requests"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    device_type = Column(String(100), nullable=False)
    device_brand = Column(String(100))
    device_model = Column(String(100))
    issue_description = Column(Text, nullable=False)
    urgency = Column(String(20), default="normal")  # low, normal, high, urgent
    estimated_cost = Column(Float)
    status = Column(String(20), default="submitted")  # submitted, in_progress, completed, cancelled
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    notes = Column(Text)
    technician_notes = Column(Text)

    def __repr__(self):
        return f"<RepairRequest(id={self.id}, customer_name='{self.customer_name}', device_type='{self.device_type}', status='{self.status}')>"