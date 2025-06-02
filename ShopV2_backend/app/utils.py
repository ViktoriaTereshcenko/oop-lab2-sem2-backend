import logging
from typing import Optional, Dict, Any
from urllib.parse import parse_qs
from fastapi import Request, HTTPException, status
from app.crud import user_crud as user_crud

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def redirect_response(location: str):
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=location, status_code=status.HTTP_303_SEE_OTHER)

async def parse_form_data(request: Request) -> Dict[str, str]:
    try:
        body = await request.body()
        data = parse_qs(body.decode())
        return {k: v[0] for k, v in data.items()}
    except Exception as e:
        logger.error(f"Failed to parse POST data: {e}")
        return {}

def safe_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

async def check_access(
    request: Request,
    required_role: Optional[str] = None
) -> int:
    user_id = request.state.user_id
    if not user_id:
        logger.warning("Access denied: no authenticated user")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    user = user_crud.get_user_by_id(request.app.state.db, user_id)
    if not user:
        logger.warning(f"Access denied: user {user_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if required_role and user.role != required_role:
        logger.warning(f"Access denied: user role '{user.role}' insufficient (required: '{required_role}')")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return user_id
