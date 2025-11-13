from pydantic import BaseModel
from datetime import datetime



class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone: str


class UserUpdate(BaseModel):
    name: str
    phone: str


class User(BaseModel):
    id: str
    name: str
    email: str
    password: str
    phone: str
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str













