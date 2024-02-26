from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserUpdate(BaseModel):
    name: str
    email: str

class BookCreate(BaseModel):
    title: str
    author: str
    description: str

class BookUpdate(BaseModel):
    title: str
    author: str