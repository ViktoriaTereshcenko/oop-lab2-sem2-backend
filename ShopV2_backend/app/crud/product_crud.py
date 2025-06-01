from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional, cast
from app.models.product_model import Product
from app.schemas.product_scheme import ProductCreate, ProductUpdate

def get_all_products(db: Session) -> List[Product]:
    products = db.query(Product).all()
    return cast(List[Product], products)

def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(and_(Product.id == product_id)).first()

def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
    product = db.query(Product).filter(and_(Product.id == product_id)).first()
    if product:
        for key, value in product_data.model_dump().items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
    return product

def delete_product(db: Session, product_id: int) -> Optional[Product]:
    product = db.query(Product).filter(and_(Product.id == product_id)).first()
    if product:
        db.delete(product)
        db.commit()
    return product
