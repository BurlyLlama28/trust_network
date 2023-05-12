from typing import List

from fastapi import APIRouter

from app.cruds.comment_crud import (create_child_comment, create_comment,
                                    delete_comment, edit_comment,
                                    get_post_comments)
from app.schemas import Comment, CommentOptional

comment_router = APIRouter()

@comment_router.post("", response_model = Comment, status_code = 201)
async def new_comment(comment: Comment):
    return await create_comment(post_id=comment.post_id, content=comment.content, author_id=comment.author_id)

@comment_router.patch("/{author_id}/{id}", response_model = Comment, status_code = 200)
async def update_comment(author_id: int, id: int, post: CommentOptional):
    return await edit_comment(id=id, author_id=author_id, content=post.content)

@comment_router.post("/{author_id}/{id}/reply", response_model=List[Comment], status_code=201)
async def reply_on_comment(author_id: int, id: int, comment: CommentOptional):
    return await create_child_comment(authour_id=author_id, id=id, comment=comment)

@comment_router.delete('/{id}', status_code=200)
async def remove_comment(id: int):
    return await delete_comment(id = id)

@comment_router.get("/{post_id}", status_code=200)
async def receive_post_comments(post_id: int):
    return await get_post_comments(id = post_id)