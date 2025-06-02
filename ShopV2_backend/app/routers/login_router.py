from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db
from app.auth.jwt_handler import create_access_token
from app.crud.user_crud import get_user_by_credentials
import logging

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")
logger = logging.getLogger(__name__)

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = get_user_by_credentials(db, username=username, password=password)
    if not user:
        logger.warning(f"Login failed for username '{username}'")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Incorrect login or password"
        }, status_code=401)

    token = create_access_token(user.id)
    logger.info(f"User '{username}' logged in successfully")

    response = RedirectResponse(url="/index", status_code=303)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True, max_age=86400)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("access_token")
    logger.info("User logged out")
    return response
