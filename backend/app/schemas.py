from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role_id: Optional[int] = None


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role_id: Optional[int]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginData(BaseModel):
    email: str
    password: str


class ProjectCreate(BaseModel):
    name: str


class ProjectOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class RFPOut(BaseModel):
    id: int
    filename: str

    class Config:
        orm_mode = True
