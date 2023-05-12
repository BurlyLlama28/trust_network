from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


def create_app() -> FastAPI:

    app = FastAPI(docs_url="/")

    register_tortoise(
        app,
        db_url="asyncpg://postgres:@localhost:5432/postgres",
        modules={"models": ["app.models"]},
        generate_schemas=True,
    )

    register_routers(app=app)

    return app

def register_routers(app: FastAPI):
    from app.routers import authors, comments, posts
    app.include_router(authors.author_router)
    app.include_router(posts.post_router)
    app.include_router(comments.comment_router)