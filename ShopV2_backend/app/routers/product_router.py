from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db, get_current_user, require_admin
from app.models.user_model import User
from app.crud import product_crud
from app.schemas.product_scheme import ProductCreate
import logging

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")
logger = logging.getLogger(__name__)

@router.get("/products", response_class=HTMLResponse)
def list_products(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    products = product_crud.get_all_products(db)
    return templates.TemplateResponse("products/list.html", {
        "request": request,
        "products": products,
        "username": current_user.username
    })

@router.get("/products/create", response_class=HTMLResponse)
def create_form(request: Request, current_user: User = Depends(require_admin)):
    return templates.TemplateResponse("product_form.html", {
        "request": request,
        "username": current_user.username
    })

@router.post("/products/create")
def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    try:
        product_data = ProductCreate(name=name, description=description, price=price)
        product_crud.create_product(db, product_data)
        logger.info(f"Product '{name}' created by admin '{current_user.username}'")
    except Exception as e:
        logger.warning(f"Failed to create product: {e}")
    return RedirectResponse(url="/products", status_code=303)

@router.get("/products/delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    product_crud.delete_product(db, product_id)
    logger.info(f"Product with ID {product_id} deleted by admin '{current_user.username}'")
    return RedirectResponse(url="/products", status_code=303)
