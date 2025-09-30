from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

class RepairRequestBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=255)
    customer_email: EmailStr
    customer_phone: str = Field(..., max_length=20)
    device_type: str = Field(..., min_length=1, max_length=100)
    device_brand: Optional[str] = Field(None, max_length=100)
    device_model: Optional[str] = Field(None, max_length=100)
    issue_description: str = Field(..., min_length=1)
    urgency: str = Field(default="normal", max_length=20)

class RepairRequestCreate(RepairRequestBase):
    pass

class RepairRequestUpdate(BaseModel):
    urgency: Optional[str] = Field(None, max_length=20)
    estimated_cost: Optional[float] = Field(None, ge=0)
    status: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = None
    technician_notes: Optional[str] = None

class RepairRequest(RepairRequestBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    estimated_cost: Optional[float] = None
    status: str
    submitted_at: datetime
    updated_at: datetime
    notes: Optional[str] = None
    technician_notes: Optional[str] = None