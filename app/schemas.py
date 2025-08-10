from typing import Optional
from pydantic import ConfigDict, HttpUrl, BaseModel, EmailStr
from datetime import datetime


class URLBase(BaseModel):
    long_url: str


class Urlryic(BaseModel):
    long_url: str


class UserBase(BaseModel):
    email: EmailStr
    password: str
    username:str
    status: Optional[bool] = False
    FirstLogin:Optional[bool] = False


class UserCreate(UserBase):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username:str
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class RegistrationUserRepsonse(BaseModel):
    message: str
    data: UserResponse
