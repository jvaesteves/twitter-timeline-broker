from typing import TypeAlias

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from ._helpers import uuid_factory
from .user import User


class Tweet(Model):
    id = fields.UUIDField(pk=True, default=uuid_factory)
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User",
        to_field="id",
    )
    text = fields.CharField(max_length=280)


TweetPydantic: TypeAlias = pydantic_model_creator(Tweet, name="Tweet")  # type: ignore[misc]
