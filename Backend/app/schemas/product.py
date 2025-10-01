from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: str = Field(..., min_length=1, max_length=100)
    sub_category: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    price: float = Field(..., gt=0)
    original_price: Optional[float] = Field(None, gt=0)
    stock: int = Field(default=0, ge=0)
    sku: Optional[str] = Field(None, max_length=100)
    warranty: Optional[str] = Field(None, max_length=100)
    condition: str = Field(default="new", max_length=50)
    tags: Optional[List[str]] = None
    
    # Tech specs
    processor: Optional[str] = Field(None, max_length=100)
    ram: Optional[str] = Field(None, max_length=50)
    storage: Optional[str] = Field(None, max_length=50)
    storage_type: Optional[str] = Field(None, max_length=50)
    graphics: Optional[str] = Field(None, max_length=100)
    screen_size: Optional[str] = Field(None, max_length=50)
    os: Optional[str] = Field(None, max_length=100)
    camera: Optional[str] = Field(None, max_length=100)
    battery: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=50)
    weight: Optional[str] = Field(None, max_length=50)
    dimensions: Optional[str] = Field(None, max_length=100)
    connectivity: Optional[str] = Field(None, max_length=100)
    additional_specs: Optional[dict] = None
    
    images: Optional[List[str]] = None
    status: str = Field(default="active", max_length=20)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    sub_category: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    original_price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    sku: Optional[str] = Field(None, max_length=100)
    warranty: Optional[str] = Field(None, max_length=100)
    condition: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = None
    
    # Tech specs
    processor: Optional[str] = Field(None, max_length=100)
    ram: Optional[str] = Field(None, max_length=50)
    storage: Optional[str] = Field(None, max_length=50)
    storage_type: Optional[str] = Field(None, max_length=50)
    graphics: Optional[str] = Field(None, max_length=100)
    screen_size: Optional[str] = Field(None, max_length=50)
    os: Optional[str] = Field(None, max_length=100)
    camera: Optional[str] = Field(None, max_length=100)
    battery: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=50)
    weight: Optional[str] = Field(None, max_length=50)
    dimensions: Optional[str] = Field(None, max_length=100)
    connectivity: Optional[str] = Field(None, max_length=100)
    additional_specs: Optional[dict] = None
    
    images: Optional[List[str]] = None
    status: Optional[str] = Field(None, max_length=20)

class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime