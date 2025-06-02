from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db, get_current_user
from app.models.user_model import User
from app.crud import order_crud, product_crud
from app.schemas.order_scheme import OrderCreate
import logging

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")
logger = logging.getLogger(__name__)

@router.get("/orders", response_class=HTMLResponse)
def list_orders(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = order_crud.get_orders_by_user(db, current_user.id)
    return templates.TemplateResponse("orders.html", {
        "request": request,
        "orders": orders,
        "username": current_user.username
    })

@router.get("/orders/create", response_class=HTMLResponse)
def create_form(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    products = product_crud.get_all_products(db)
    return templates.TemplateResponse("order_form.html", {
        "request": request,
        "products": products,
        "username": current_user.username
    })

@router.post("/orders/create")
def create_order(
    product_id: int = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        order_data = OrderCreate(product_id=product_id, quantity=quantity)
        order_crud.create_order(db, order_data, current_user.id)
        logger.info(f"User {current_user.id} created order for product {product_id}")
    except Exception as e:
        logger.warning(f"Failed to create order: {e}")
    return RedirectResponse(url="/orders", status_code=303)

@router.get("/orders/pay/{order_id}")
def pay_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = order_crud.mark_order_paid(db, order_id)
    if order:
        logger.info(f"User {current_user.id} paid for order {order_id}")
    else:
        logger.warning("Invalid order_id in payment")
    return RedirectResponse(url="/orders", status_code=303)
