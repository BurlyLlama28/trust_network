from fastapi import Query

from app.models import Comment


async def create_comment(post_id: int, content: str, author_id: int) -> Comment:
    new_comment =  await Comment.create(post_id = post_id, content = content, author_id = author_id)
    return new_comment

async def edit_comment(id : int, author_id: int, content: str) -> Comment:
    await Comment.filter(author_id = author_id, id = id).update(**{"content": content})
    return await Comment.get(id = id)

async def create_child_comment(authour_id: int, id: int, comment: Comment) -> list[Comment]:
    new_comment = await Comment.create(post_id = comment.post_id, content = comment.content, parent_comment_id = id, author_id = authour_id)
    return await get_comment_thread(comment_id = new_comment.id)

async def delete_comment(id: int) -> None:
    comment = await Comment.get(id = id)
    if comment.parent_comment_id is not None:
        await Comment.filter(parent_comment_id = id).update(**{"parent_comment_id": comment.parent_comment_id})
    else:
        await Comment.filter(parent_comment_id = id).update(**{"parent_comment_id": None})
    await comment.delete()

async def get_top_level_comments(id: int) ->list[Comment]:
    return await check_childen_availability(
        comments = await Comment.filter(post_id=id, parent_comment_id=None).order_by("created_at").all()
    )


async def get_comment_thread(comment_id: int) -> list[Comment]:
    comments: list = []
    current_comment = await Comment.get(id=comment_id)
    if current_comment:
        comments.append(current_comment)
        while current_comment.parent_comment:
            current_comment = await current_comment.parent_comment
            comments.insert(0, current_comment)
    return comments

async def get_child_comments(comment_id: int) -> list[(Comment, bool)]:
    return await check_childen_availability(comments= await Comment.filter(parent_comment_id=comment_id).all())

async def check_childen_availability(comments: list[Comment]) -> list[(Comment, bool)]:
    comments_with_childs = []
    for comment in comments:
        has_childs = await Comment.filter(parent_comment_id=comment.id).exists()
        comments_with_childs.append((comment, has_childs))
    return comments_with_childs
