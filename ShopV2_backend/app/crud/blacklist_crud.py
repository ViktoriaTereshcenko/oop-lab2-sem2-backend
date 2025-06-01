from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.models.blacklist_model import Blacklist
from app.models.user_model import User
from typing import List
from datetime import datetime, timezone
from app.schemas.blacklist_scheme import BlacklistOut

def add_to_blacklist(db: Session, user_id: int, reason: str) -> Blacklist:
    blacklisted = Blacklist(
        user_id=user_id,
        reason=reason,
        created_at=datetime.now(timezone.utc)
    )
    db.add(blacklisted)
    db.commit()
    db.refresh(blacklisted)
    return blacklisted

def is_user_blacklisted(db: Session, user_id: int) -> bool:
    stmt = select(Blacklist).where(Blacklist.user_id.op('=')(user_id))
    result = db.execute(stmt).scalar_one_or_none()
    return result is not None

def get_blacklist(db: Session) -> List[BlacklistOut]:
    stmt = (
        select(User.username, Blacklist.reason, Blacklist.created_at)
        .join(User, and_(Blacklist.user_id == User.id))
        .order_by(Blacklist.created_at.desc())
    )
    result = db.execute(stmt).all()

    return [
        BlacklistOut(username=username, reason=reason, created_at=created_at)
        for username, reason, created_at in result
    ]

def remove_user_from_blacklist(db: Session, user_id: int) -> None:
    stmt = select(Blacklist).where(Blacklist.user_id.op('=')(user_id))
    result = db.execute(stmt).scalar_one_or_none()
    if result:
        db.delete(result)
        db.commit()
