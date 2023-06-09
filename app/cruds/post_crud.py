from app.models import Post


async def create_post(title: str, body: str, author_id: int) -> Post:
    new_post =  await Post.create(title = title, body = body, author_id = author_id)
    return new_post

async def edit_post(id : int, author_id: int, **kwargs) -> Post:
    await Post.filter(author_id = author_id, id = id).update(**kwargs)
    return await get_post(id = id)

async def get_post(id: int) -> Post:
    return await Post.get(id = id)

async def get_posts(limit: int , offset: int ) -> list[Post]:
    posts = await Post.all().limit(limit).offset(offset)
    return posts

async def delete_post(id: int) -> None:
    post = await get_post(id = id)
    await post.delete()
