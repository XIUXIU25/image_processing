from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    username: str

class UserCreate(BaseModel):
    username: str
    password: str

class ImageMeta(BaseModel):
    id: int
    filename: str
    url: str
    uploaded_by: int