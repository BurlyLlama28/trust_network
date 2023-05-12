from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from pydantic import validator as pyd_validator
from pydantic.main import BaseModel


def convert_to_optional(schema):
    return {k: Optional[v] for k, v in schema.__annotations__.items()}

class PasswordLengthError(Exception):
    """Custom error that is raised when password is too small"""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class Author(BaseModel):
    """Represents author object in DB"""
    id: Optional[int]
    name: str
    email: EmailStr
    password: str

    
    @pyd_validator("password")
    @classmethod
    def password_valid(cls, value) -> None:
        """Check whether password length is >= 8 symbols"""
        if len(value) < 8:
            raise PasswordLengthError(
                value=value, message="Password should be at least 8 characters long"
            )
        return value
    
    class Config:
        orm_mode = True


class Comment(BaseModel):
    """Represent Comment object in DB"""
    id: Optional[int]
    post_id : int
    parent_comment_id : int = None
    content : str
    author_id : int
    created_at : datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class Post(BaseModel):
    """Represent Post object in DB"""
    id: Optional[int]
    title : str
    body : str
    author_id : int

    class Config:
        orm_mode = True

class PostOptional(Post):
    __annotations__ = convert_to_optional(Post)

class CommentOptional(Comment):
    __annotations__ = convert_to_optional(Comment)