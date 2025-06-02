from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db
from app.schemas.user_scheme import UserCreate
from app.crud.user_crud import create_user, get_user_by_credentials
from app.auth.jwt_handler import create_access_token
import logging

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")
logger = logging.getLogger(__name__)

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

    if get_user_by_credentials(db, username=username, password=password):
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "The user already exists."
        }, status_code=409)

    try:
        user = create_user(db, UserCreate(username=username, password=password, role="user"))
        token = create_access_token(user.id)
        logger.info(f"User '{username}' successfully registered.")

        response = RedirectResponse(url="/index", status_code=303)
        response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True, max_age=86400)
        return response
    except Exception as e:
        logger.error(f"Error during registration: {e}")
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Failed to register user."
        }, status_code=500)
