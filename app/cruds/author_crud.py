from app.models import Author


async def register_author(name: str, email: str, password: str) -> Author:
    new_author = await Author.create(name = name, email = email, password = password)
    return new_author

async def change_author_password(id: int, password: str) -> Author:
    await Author.filter(id = id).update(**{"password": password})
    return await get_author(id = id)

async def change_author_name(name: str, id: int) -> Author:
    await Author.filter(id = id).update(**{"name": name})
    return await get_author(id = id)

async def get_author(id: int) -> Author:
    return await Author.get(id = id)
