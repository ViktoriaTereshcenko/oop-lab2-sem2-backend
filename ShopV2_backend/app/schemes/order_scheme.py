from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderCreate(BaseModel):
    product_id: int
    quantity: int
    is_paid: Optional[bool] = False

class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    is_paid: bool
    created_at: datetime

    class Config:
        orm_mode = True
