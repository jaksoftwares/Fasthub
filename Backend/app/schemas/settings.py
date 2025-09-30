from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any

class SettingsBase(BaseModel):
    store_name: str = Field(default="My E-Commerce Store", max_length=255)
    store_description: Optional[str] = Field(None, max_length=500)
    contact_email: Optional[str] = Field(None, max_length=255)
    contact_phone: Optional[str] = Field(None, max_length=20)
    address: Optional[Dict[str, Any]] = None
    currency: str = Field(default="KES", max_length=10)
    tax_rate: float = Field(default=0.16, ge=0, le=1)
    free_shipping_threshold: float = Field(default=1000.0, ge=0)

class PaymentSettings(BaseModel):
    mpesa_enabled: bool = True
    card_enabled: bool = True
    cod_enabled: bool = True
    mpesa_shortcode: Optional[str] = Field(None, max_length=20)
    mpesa_passkey: Optional[str] = Field(None, max_length=255)
    mpesa_consumer_key: Optional[str] = Field(None, max_length=255)
    mpesa_consumer_secret: Optional[str] = Field(None, max_length=255)

class ShippingSettings(BaseModel):
    standard_fee: float = Field(default=200.0, ge=0)
    express_fee: float = Field(default=500.0, ge=0)
    free_enabled: bool = True
    same_day_enabled: bool = False

class NotificationSettings(BaseModel):
    email_enabled: bool = True
    sms_enabled: bool = True
    order_confirmations: bool = True
    low_stock_alerts: bool = True
    new_order_alerts: bool = True

class SettingsCreate(SettingsBase):
    payment: Optional[PaymentSettings] = None
    shipping: Optional[ShippingSettings] = None
    notifications: Optional[NotificationSettings] = None

class SettingsUpdate(BaseModel):
    store_name: Optional[str] = Field(None, max_length=255)
    store_description: Optional[str] = Field(None, max_length=500)
    contact_email: Optional[str] = Field(None, max_length=255)
    contact_phone: Optional[str] = Field(None, max_length=20)
    address: Optional[Dict[str, Any]] = None
    currency: Optional[str] = Field(None, max_length=10)
    tax_rate: Optional[float] = Field(None, ge=0, le=1)
    free_shipping_threshold: Optional[float] = Field(None, ge=0)
    payment: Optional[PaymentSettings] = None
    shipping: Optional[ShippingSettings] = None
    notifications: Optional[NotificationSettings] = None

class Settings(SettingsBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    payment: PaymentSettings
    shipping: ShippingSettings
    notifications: NotificationSettings