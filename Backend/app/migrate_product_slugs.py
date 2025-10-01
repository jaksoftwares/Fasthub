from app.config import SessionLocal
from app.models.product import Product
import re

def slugify(name: str) -> str:
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug

def migrate_product_slugs():
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        seen = set()
        for product in products:
            if not product.slug or product.slug.isdigit():
                base_slug = slugify(product.name)
                slug = base_slug
                i = 2
                # Ensure uniqueness
                while slug in seen or db.query(Product).filter(Product.slug == slug, Product.id != product.id).first():
                    slug = f"{base_slug}-{i}"
                    i += 1
                product.slug = slug
                seen.add(slug)
                print(f"Updated product id={product.id} name='{product.name}' to slug='{slug}'")
        db.commit()
        print("Slug migration complete.")
    except Exception as e:
        print(f"Error during slug migration: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_product_slugs()
