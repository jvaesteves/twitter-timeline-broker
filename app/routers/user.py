from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from ..models import User, UserPydantic

router = APIRouter(prefix="/user")


@router.get("/", response_model=List[UserPydantic])
async def get_users():
    return await UserPydantic.from_queryset(User.all())


@router.post("/", response_model=UserPydantic)
async def create_user(user: UserPydantic):
    created_user = await User.create(**user.dict(exclude_unset=True))
    return await UserPydantic.from_tortoise_orm(created_user)


@router.get(
    "/{user_id}",
    response_model=UserPydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_user(user_id: UUID):
    return await UserPydantic.from_queryset_single(User.get(id=user_id))


@router.put(
    "/{user_id}",
    response_model=UserPydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_user(user_id: UUID, user: UserPydantic):
    await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await UserPydantic.from_queryset_single(User.get(id=user_id))


@router.delete(
    "/{user_id}",
    responses={404: {"model": HTTPNotFoundError}},
)
async def delete_user(user_id: UUID):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    return {"message": f"Deleted user '{user_id}'"}
