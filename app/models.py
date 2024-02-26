from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(50), index=True)
    email: str = Column(String(50), unique=True, index=True)
    password: str = Column(String(50))
    
class Book(Base):
    __tablename__ = "posts"

    id: int = Column(Integer, primary_key=True, nullable=False)
    title: str = Column(String, nullable=False)
    author: str = Column(String, nullable=False)
    description: str = Column(String, nullable=False)