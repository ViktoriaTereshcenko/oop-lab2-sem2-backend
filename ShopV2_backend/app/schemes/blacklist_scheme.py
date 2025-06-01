from pydantic import BaseModel
from datetime import datetime

class BlacklistCreate(BaseModel):
    user_id: int
    reason: str

class BlacklistOut(BaseModel):
    username: str
    reason: str
    created_at: datetime

    class Config:
        orm_mode = True
