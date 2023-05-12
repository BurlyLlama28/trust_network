from fastapi import APIRouter, Query

from app.cruds.post_crud import (create_post, delete_post, edit_post, get_post,
                                 get_posts)
from app.schemas import Post, PostOptional

post_router = APIRouter(prefix="/posts", tags=["Posts"])

@post_router.post("/new", status_code = 201)
async def new_post(post: Post) -> Post:
    return await create_post(title = post.title, body = post.body, author_id = post.author_id)

@post_router.patch("/{author_id}/{id}", status_code = 200)
async def update_post(author_id: int, id: int, post: PostOptional) -> Post:
    updated_values: dict =  {name: value for name, value in post.dict().items() if value is not None}
    return await edit_post(id=id, author_id=author_id, **updated_values)

@post_router.get("/{id}", status_code=200)
async def receive_post(id: int) -> Post:
    return await get_post(id = id)

@post_router.get("", status_code=200)
async def receive_posts(limit: int = Query(10, gt=0), offset: int = Query(0, ge=0)) -> list[Post]:
    return await get_posts(limit = limit, offset = offset)

@post_router.delete("/{id}", status_code=200)
async def remove_post(id: int) -> None:
    return await delete_post(id = id)