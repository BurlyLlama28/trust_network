from fastapi import APIRouter

from app.cruds.author_crud import (change_author_name, change_author_password,
                                   get_author, register_author)
from app.schemas import Author

author_router = APIRouter(prefix="/author", tags=["Authors"])

@author_router.post("", status_code=201)
async def new_author(author: Author) -> Author:
    return await register_author(name = author.name, email = author.email, password = author.password)

@author_router.patch("/{id}/name", status_code=200)
async def edit_author_name(author_id: int, name: str) -> Author:
    return await change_author_name(name = name, id = author_id)

@author_router.patch("/{id}/password", status_code=200)
async def edit_author_password(author_id: int, password: str) -> Author:
    return await change_author_password(password = password, id = author_id)

@author_router.get("/{id}", status_code=200)
async def get_author_info(author_id: int) -> Author:
    return await get_author(id = author_id)
