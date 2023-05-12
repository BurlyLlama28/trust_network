from typing import List

from fastapi import Query

from app.models import Comment


async def create_comment(post_id: int, content: str, author_id: int) -> Comment:
    new_comment =  await Comment.create(post_id = post_id, content = content, author_id = author_id)
    return new_comment

async def edit_comment(id : int, author_id: int, content: str) -> Comment:
    await Comment.filter(author_id = author_id, id = id).update(**{"content": content})
    return await Comment.get_or_none(id = id)

async def create_child_comment(authour_id: int, id: int, comment: Comment) -> List[Comment]:
    new_comment = await Comment.create(post_id = comment.post_id, content = comment.content, parent_comment_id = id, author_id = authour_id)
    return await get_comment_thread(comment_id = new_comment.id)

async def delete_comment(id: int) -> None:
    comment = await Comment.get_or_none(id = id)
    if comment.parent_comment_id is not None:
        await Comment.filter(parent_comment_id = id).update(**{"parent_comment_id": comment.parent_comment_id})
    else:
        await Comment.filter(parent_comment_id = id).update(**{"parent_comment_id": None})
    await comment.delete()

async def get_post_comments(id: int) ->List[List[Comment]]:
    top_level_comments: list = [x for x in await Comment.filter(post_id=id, parent_comment_id=None).order_by("created_at").all()]
    print("TEST", top_level_comments)
    all_comments: list[list] = []
    for comment in top_level_comments:
        new_thread = await get_comment_thread_bottom(comment)
        all_comments.append([comment, new_thread])
    print("ALL COMMENTS!!!!!!", all_comments)
    return all_comments


async def get_comment_thread(comment_id: int) -> List[Comment]:
    comments: list = []
    current_comment = await Comment.get_or_none(id=comment_id)
    if current_comment:
        comments.append(current_comment)
        while current_comment.parent_comment:
            current_comment = await current_comment.parent_comment
            comments.insert(0, current_comment)
    return comments

async def get_comment_thread_bottom(comment: Comment) -> List[Comment]:
    comment_thread: list = [comment, ]
    comment_thread = await _fetch_child_comments(parent_comment_id=comment.id)
    return comment_thread

async def _fetch_child_comments(parent_comment_id: int) -> None:
    child_comments = await Comment.filter(parent_comment_id=parent_comment_id).all()
    comments = []
    for comment in child_comments:
        child_of_child_comments = await _fetch_child_comments(parent_comment_id=comment.id)
        comments.append([comment, child_of_child_comments])
    return comments
