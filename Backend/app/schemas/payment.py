from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    order_id: int
    method: str = Field(..., max_length=50)
    amount: float = Field(..., gt=0)
    phone_number: Optional[str] = Field(None, max_length=20)

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=20)
    transaction_id: Optional[str] = Field(None, max_length=255)

class Payment(PaymentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    status: str
    transaction_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class MpesaSTKRequest(BaseModel):
    phone_number: str = Field(..., pattern=r'^254\d{9}$')
    amount: float = Field(..., gt=0)
    order_id: int
    account_reference: str = Field('Fasthub Computers', max_length=20)
    transaction_desc: str = Field('Fasthub Computers', max_length=50)

class MpesaCallback(BaseModel):
    MerchantRequestID: str
    CheckoutRequestID: str
    ResultCode: int
    ResultDesc: str
    CallbackMetadata: Optional[dict] = None