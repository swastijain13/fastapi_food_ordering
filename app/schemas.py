from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class SignupRequest(BaseModel):
    username: str
    password: str
    email : str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    email: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)


class MenuItemCreate(BaseModel):
    name: str
    price: int


class MenuItemResponse(BaseModel):
    name: str
    price: int

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    menu_id: int
    quantity: int

class OrderResponse(BaseModel):
    id: int
    user_id: int
    menu_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)

