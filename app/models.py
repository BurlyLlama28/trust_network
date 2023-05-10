from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField
from tortoise.models import Model


class Author(Model):
    """Model-class of author table in database"""
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique = True)
    password = fields.CharField(max_length=100)

    class Meta:
        table = "authors"

class Comment(Model):
    post = fields.ForeignKeyField("models.Post", related_name="comments")
    parent_comment = fields.ForeignKeyField("models.Comment", related_name="replies", null = True)
    content = fields.TextField()
    author = fields.ForeignKeyField("models.Author", related_name="comments")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "comments"

class Post(Model):
    title = fields.CharField(max_length=100)
    body = fields.TextField()
    author = fields.ForeignKeyField("models.Author", related_name="posts")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "posts"
