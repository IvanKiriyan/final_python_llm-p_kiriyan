from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserPublic(BaseModel): #описана публичная схема пользователя
    model_config = {"from_attributes": True}

    id: int
    email: EmailStr
    role: str
    created_at: datetime