from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.models.order_model import Order
from app.schemas.order_scheme import OrderCreate
from typing import List, Optional, cast

def get_all_orders(db: Session) -> List[Order]:
    result = db.scalars(select(Order).order_by(Order.created_at.desc()))
    return cast(List[Order], list(result))

def get_orders_by_user(db: Session, user_id: int) -> List[Order]:
    result = db.scalars(
        select(Order)
        .where(and_(Order.user_id == user_id))
        .order_by(Order.created_at.desc())
    )
    return cast(List[Order], list(result))

def create_order(db: Session, order: OrderCreate, user_id: int) -> Order:
    db_order = Order(
        user_id=user_id,
        product_id=order.product_id,
        quantity=order.quantity,
        is_paid=bool(order.is_paid)
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def mark_order_paid(db: Session, order_id: int) -> Optional[Order]:
    db_order = db.get(Order, order_id)
    if db_order:
        db_order.is_paid = True
        db.commit()
        db.refresh(db_order)
    return db_order

def update_payment_status(db: Session, order_id: int, is_paid: bool) -> Optional[Order]:
    db_order = db.get(Order, order_id)
    if db_order:
        db_order.is_paid = is_paid
        db.commit()
        db.refresh(db_order)
    return db_order
