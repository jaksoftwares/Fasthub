    # Removed stray top-level get_product_by_slug definition
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    @staticmethod
    def get_product_by_slug(db: Session, slug: str) -> Optional[Product]:
        return db.query(Product).filter(Product.slug == slug).first()

    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> Product:
        # Check for duplicate SKU
        if product.sku:
            existing = ProductService.get_product_by_sku(db, product.sku)
            if existing:
                raise Exception(f"A product with SKU '{product.sku}' already exists.")
        # Ensure slug is present and unique, auto-generate if missing
        slug = product.slug if getattr(product, 'slug', None) else ProductService.slugify(product.name)
        # Ensure slug is unique
        existing_slug = ProductService.get_product_by_slug(db, slug)
        if existing_slug:
            # If slug exists, append a number to make it unique
            base_slug = slug
            i = 2
            while ProductService.get_product_by_slug(db, f"{base_slug}-{i}"):
                i += 1
            slug = f"{base_slug}-{i}"
        db_product = Product(**{**product.model_dump(), 'slug': slug})
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def slugify(name: str) -> str:
        import re
        slug = name.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')
        return slug
    
    @staticmethod
    def get_product(db: Session, product_id: int) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()
    
    @staticmethod
    def get_product_by_sku(db: Session, sku: str) -> Optional[Product]:
        return db.query(Product).filter(Product.sku == sku).first()
    
    @staticmethod
    def get_products(db: Session, skip: int = 0, limit: int = 100, category: Optional[str] = None, 
                    status: Optional[str] = None) -> List[Product]:
        query = db.query(Product)
        
        if category:
            query = query.filter(Product.category == category)
        if status:
            query = query.filter(Product.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def search_products(db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[Product]:
        from sqlalchemy import or_
        return db.query(Product).filter(
            or_(
                Product.name.contains(search_term),
                Product.description.contains(search_term),
                Product.brand.contains(search_term)
            )
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
        db_product = ProductService.get_product(db, product_id)
        if not db_product:
            return None
        
        update_data = product_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        db_product = ProductService.get_product(db, product_id)
        if not db_product:
            return False
        
        db.delete(db_product)
        db.commit()
        return True
    
    @staticmethod
    def update_stock(db: Session, product_id: int, quantity_change: int) -> Optional[Product]:
        db_product = ProductService.get_product(db, product_id)
        if not db_product:
            return None
        
        new_stock = db_product.stock + quantity_change
        if new_stock < 0:
            return None  # Insufficient stock
        
        setattr(db_product, 'stock', new_stock)
        db.commit()
        db.refresh(db_product)
        return db_product