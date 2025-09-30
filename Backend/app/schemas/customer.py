from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)

class CustomerCreate(CustomerBase):
    password: str = Field(..., min_length=6)

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    password: Optional[str] = Field(None, min_length=6)
    status: Optional[str] = Field(None, max_length=20)

class Customer(CustomerBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    total_orders: int
    total_spent: float
    status: str
    join_date: datetime
    last_order: Optional[datetime] = None