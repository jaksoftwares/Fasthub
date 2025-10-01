from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import get_db
from app.schemas.settings import Settings, SettingsCreate, SettingsUpdate
from app.models.settings import Settings as SettingsModel

router = APIRouter(prefix="/settings", tags=["settings"])

@router.post("/", response_model=Settings)
def create_settings(settings: SettingsCreate, db: Session = Depends(get_db)):
    # Check if settings already exist
    existing_settings = db.query(SettingsModel).first()
    if existing_settings:
        raise HTTPException(status_code=400, detail="Settings already exist. Use PUT to update.")
    
    # Convert nested objects to flat structure for database storage
    settings_data = settings.model_dump()
    payment_data = settings_data.pop("payment", {})
    shipping_data = settings_data.pop("shipping", {})
    notifications_data = settings_data.pop("notifications", {})
    
    # Flatten payment settings
    for key, value in payment_data.items():
        settings_data[f"payment_{key}"] = value
    
    # Flatten shipping settings
    for key, value in shipping_data.items():
        settings_data[f"shipping_{key}"] = value
    
    # Flatten notification settings
    for key, value in notifications_data.items():
        settings_data[f"notifications_{key}"] = value
    
    db_settings = SettingsModel(**settings_data)
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    # Reconstruct nested objects for response (same as GET)
    payment = {
        "mpesa_enabled": db_settings.payment_mpesa_enabled,
        "card_enabled": db_settings.payment_card_enabled,
        "cod_enabled": db_settings.payment_cod_enabled,
        "mpesa_shortcode": db_settings.payment_mpesa_shortcode,
        "mpesa_passkey": db_settings.payment_mpesa_passkey,
        "mpesa_consumer_key": db_settings.payment_mpesa_consumer_key,
        "mpesa_consumer_secret": db_settings.payment_mpesa_consumer_secret,
    }
    shipping = {
        "standard_fee": db_settings.shipping_standard_fee,
        "express_fee": db_settings.shipping_express_fee,
        "free_enabled": db_settings.shipping_free_enabled,
        "same_day_enabled": db_settings.shipping_same_day_enabled,
    }
    notifications = {
        "email_enabled": db_settings.notifications_email_enabled,
        "sms_enabled": db_settings.notifications_sms_enabled,
        "order_confirmations": db_settings.notifications_order_confirmations,
        "low_stock_alerts": db_settings.notifications_low_stock_alerts,
        "new_order_alerts": db_settings.notifications_new_order_alerts,
    }
    response = {
        **db_settings.__dict__,
        "payment": payment,
        "shipping": shipping,
        "notifications": notifications,
    }
    response.pop("_sa_instance_state", None)
    return response

@router.get("/", response_model=Settings)
def get_settings(db: Session = Depends(get_db)):
    settings = db.query(SettingsModel).first()
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    # Reconstruct nested objects for response
    payment = {
        "mpesa_enabled": settings.payment_mpesa_enabled,
        "card_enabled": settings.payment_card_enabled,
        "cod_enabled": settings.payment_cod_enabled,
        "mpesa_shortcode": settings.payment_mpesa_shortcode,
        "mpesa_passkey": settings.payment_mpesa_passkey,
        "mpesa_consumer_key": settings.payment_mpesa_consumer_key,
        "mpesa_consumer_secret": settings.payment_mpesa_consumer_secret,
    }
    shipping = {
        "standard_fee": settings.shipping_standard_fee,
        "express_fee": settings.shipping_express_fee,
        "free_enabled": settings.shipping_free_enabled,
        "same_day_enabled": settings.shipping_same_day_enabled,
    }
    notifications = {
        "email_enabled": settings.notifications_email_enabled,
        "sms_enabled": settings.notifications_sms_enabled,
        "order_confirmations": settings.notifications_order_confirmations,
        "low_stock_alerts": settings.notifications_low_stock_alerts,
        "new_order_alerts": settings.notifications_new_order_alerts,
    }
    # Build response dict
    response = {
        **settings.__dict__,
        "payment": payment,
        "shipping": shipping,
        "notifications": notifications,
    }
    # Remove SQLAlchemy instance state
    response.pop("_sa_instance_state", None)
    return response

@router.put("/", response_model=Settings)
def update_settings(settings_update: SettingsUpdate, db: Session = Depends(get_db)):
    db_settings = db.query(SettingsModel).first()
    if not db_settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    
    # Convert nested objects to flat structure for database storage
    update_data = settings_update.model_dump(exclude_unset=True)
    payment_data = update_data.pop("payment", {})
    shipping_data = update_data.pop("shipping", {})
    notifications_data = update_data.pop("notifications", {})
    
    # Flatten payment settings
    for key, value in payment_data.items():
        update_data[f"payment_{key}"] = value
    
    # Flatten shipping settings
    for key, value in shipping_data.items():
        update_data[f"shipping_{key}"] = value
    
    # Flatten notification settings
    for key, value in notifications_data.items():
        update_data[f"notifications_{key}"] = value
    
    for field, value in update_data.items():
        setattr(db_settings, field, value)
    
    db.commit()
    db.refresh(db_settings)
    return db_settings