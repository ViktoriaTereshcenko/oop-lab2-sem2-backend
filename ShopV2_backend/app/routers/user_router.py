from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db, require_admin
from app.crud import user_crud
from app.schemas.user_scheme import UserCreate
import logging

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")
logger = logging.getLogger(__name__)

@router.get("/users", response_class=HTMLResponse)
def list_users(request: Request, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    users = user_crud.get_all_users(db)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if not username or not password:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "All fields are required."
        }, status_code=400)

    existing = user_crud.get_user_by_credentials(db, username=username, password=password)
    if existing:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "The user already exists."
        }, status_code=409)

    try:
        user_data = UserCreate(username=username, password=password, role="user")
        user_crud.create_user(db, user_data)
        logger.info(f"User '{username}' successfully registered.")
        return RedirectResponse(url="/login", status_code=303)
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Error creating user."
        }, status_code=500)
