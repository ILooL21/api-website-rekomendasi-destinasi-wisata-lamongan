from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Optional[str]

class UserCreate(UserBase):
    password: str
    oldPassword: Optional[str] = None

class UserResponse(UserBase):
    id_user: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class UserSchema(UserResponse):
    is_active_user: bool