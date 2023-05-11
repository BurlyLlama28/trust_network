from pydantic import EmailStr
from pydantic import validator as pyd_validator
from pydantic.main import BaseModel


class EmailStructureError(Exception):
    """Custom error that is raised when email is not correct"""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)

class PasswordLengthError(Exception):
    """Custom error that is raised when password is too small"""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class Author(BaseModel):
    """Represents author object in DB"""
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
    post = int
    parent_comment = int | None
    content = str
    author = int
    created_at = str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class Post(BaseModel):
    """Represent Post object in DB"""
    title = str
    body = str
    author = int
    created_at = str

    class Config:
        orm_mode = True