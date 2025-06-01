from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.user_model import User
from app.schemas.user_scheme import UserCreate
from typing import Optional, List, cast

def get_user_by_credentials(db: Session, username: str, password: str) -> Optional[User]:
    return db.query(User).filter(
        and_(
            User.username == username,
            User.password == password
        )
    ).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(and_(User.id == user_id)).first()

def get_all_users(db: Session) -> List[User]:
    users = db.query(User).all()
    return cast(List[User], users)

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
