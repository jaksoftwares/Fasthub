from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config import get_db
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.services.product import ProductService
from app.utils.cloudinary_utils import upload_image_to_cloudinary

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return ProductService.create_product(db, product)

@router.get("/", response_model=List[Product])
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return ProductService.get_products(db, skip=skip, limit=limit, category=category, status=status)

@router.get("/search", response_model=List[Product])
def search_products(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return ProductService.search_products(db, search_term=q, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = ProductService.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    product = ProductService.update_product(db, product_id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = ProductService.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# Endpoint to upload a product image to Cloudinary and return the URL
@router.post("/upload-image")
async def upload_product_image(file: UploadFile = File(...)):
    try:
        url = upload_image_to_cloudinary(await file.read())
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")

# Endpoint to create a product with image upload support
@router.post("/with-images", response_model=Product)
async def create_product_with_images(
    name: str = Form(...),
    description: str = Form(None),
    category: str = Form(...),
    price: float = Form(...),
    stock: int = Form(0),
    images: list[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    image_urls = []
    if images:
        for img in images:
            url = upload_image_to_cloudinary(await img.read())
            image_urls.append(url)
    product_data = {
        "name": name,
        "description": description,
        "category": category,
        "price": price,
        "stock": stock,
        "images": image_urls,
    }
    product = ProductCreate(**product_data)
    return ProductService.create_product(db, product)