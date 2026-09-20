from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .models import RoleEnum

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: RoleEnum
    department: Optional[str] = None
    status: str = "active"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
