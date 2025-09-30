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
    return db_settings

@router.get("/", response_model=Settings)
def get_settings(db: Session = Depends(get_db)):
    settings = db.query(SettingsModel).first()
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings

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