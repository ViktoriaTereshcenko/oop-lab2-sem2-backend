from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db import Base
from datetime import datetime, timezone

class Blacklist(Base):
    __tablename__ = "blacklist"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    reason = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
