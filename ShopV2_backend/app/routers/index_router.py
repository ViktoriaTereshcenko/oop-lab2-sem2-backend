from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.auth.dependencies import get_current_user
from app.models.user_model import User

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/index", response_class=HTMLResponse)
def index(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    username = current_user.username if current_user else "Користувач"
    return templates.TemplateResponse("index.html", {
        "request": request,
        "username": username
    })
