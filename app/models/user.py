from typing import TypeAlias

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from ._helpers import uuid_factory


class User(Model):
    id = fields.UUIDField(pk=True, default=uuid_factory)
    username = fields.CharField(max_length=16)
    follows: fields.ManyToManyRelation["User"] = fields.ManyToManyField(
        "models.User",
        through="followers",
        forward_key="follows_id",
        related_name="followers",
    )

    followers: fields.ReverseRelation["User"]


UserPydantic: TypeAlias = pydantic_model_creator(User, name="User")  # type: ignore[misc]
