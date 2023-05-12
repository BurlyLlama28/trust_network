from typing import List

from fastapi import APIRouter

from app.cruds.post_crud import (create_post, delete_post, edit_post, get_post,
                                 get_posts)
from app.schemas import Post, PostOptional

post_router = APIRouter()

@post_router.post("/new", response_model = Post, status_code = 201)
async def new_post(post: Post):
    return await create_post(title = post.title, body = post.body, author_id = post.author_id)

@post_router.patch("/{author_id}/{id}", response_model = Post, status_code = 200)
async def update_post(author_id: int, id: int, post: PostOptional):
    updated_values: dict =  {name: value for name, value in post.dict().items() if value is not None}
    return await edit_post(id=id, author_id=author_id, **updated_values)

@post_router.get("/{id}", response_model=Post, status_code=200)
async def receive_post(id: int):
    return await get_post(id = id)

@post_router.get("", response_model=List[Post], status_code=200)
async def receive_posts(limit: int, offset: int):
    return await get_posts(limit = limit, offset = offset)

@post_router.delete("/{id}", status_code=200)
async def remove_post(id: int):
    return await delete_post(id = id)