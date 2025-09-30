from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

class OrderItem(BaseModel):
    id: int
    name: str
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)

class OrderBase(BaseModel):
    customer_id: int
    products: List[OrderItem]
    total: float = Field(..., gt=0)
    payment_method: Optional[str] = Field(None, max_length=50)
    shipping_address: Optional[Dict[str, Any]] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=20)
    payment_method: Optional[str] = Field(None, max_length=50)
    shipping_address: Optional[Dict[str, Any]] = None

class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    status: str
    date: datetime