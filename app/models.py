from typing import Optional

from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField
from tortoise.models import Model


class Author(Model):
    """Model-class of author table in database"""
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique = True)
    password = fields.CharField(max_length=100)

    class Meta:
        table = "authors"

class Comment(Model):
    id = fields.IntField(pk=True)
    post = fields.ForeignKeyField("models.Post", related_name="comments")
    parent_comment = fields.ForeignKeyField("models.Comment", related_name="replies", null = True)
    content = fields.TextField()
    author = fields.ForeignKeyField("models.Author", related_name="comments")
    created_at = fields.DatetimeField(auto_now_add=True)
    edited_at = fields.DatetimeField(auto_now=True, null = True)

    class Meta:
        table = "comments"

class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100, unique = True)
    body = fields.TextField()
    author = fields.ForeignKeyField("models.Author", related_name="posts")
    created_at = fields.DatetimeField(auto_now_add=True)
    edited_at = fields.DatetimeField(auto_now=True, null = True)

    class Meta:
        table = "posts"
