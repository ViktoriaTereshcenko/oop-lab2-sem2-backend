from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db, require_admin
from app.crud import blacklist_crud
import logging

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")
logger = logging.getLogger(__name__)

@router.get("/blacklist", response_class=HTMLResponse)
def list_blacklist(request: Request, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    users = blacklist_crud.get_blacklist(db)
    return templates.TemplateResponse("blacklist.html", {
        "request": request,
        "users": users,
        "username": current_user.username
    })

@router.post("/blacklist/add")
def add_to_blacklist(
    user_id: int = Form(...),
    reason: str = Form(...),
    db: Session = Depends(get_db),
    _: str = Depends(require_admin)
):
    try:
        blacklist_crud.add_to_blacklist(db, user_id, reason)
        logger.info(f"User ID {user_id} added to blacklist")
    except Exception as e:
        logger.warning(f"Failed to add user to blacklist: {e}")
    return RedirectResponse(url="/blacklist", status_code=303)

@router.get("/blacklist/remove/{user_id}")
def remove_from_blacklist(user_id: int, db: Session = Depends(get_db), _: str = Depends(require_admin)):
    blacklist_crud.remove_user_from_blacklist(db, user_id)
    logger.info(f"User ID {user_id} removed from blacklist")
    return RedirectResponse(url="/blacklist", status_code=303)
