from uuid import UUID

from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError

from ..models import Tweet, TweetPydantic

router = APIRouter(prefix="/tweet")


@router.get("/", response_model=list[TweetPydantic])
async def get_tweets():
    return await TweetPydantic.from_queryset(Tweet.all())


@router.post("/", response_model=TweetPydantic)
async def create_tweet(tweet: TweetPydantic):
    created_tweet = await Tweet.create(**tweet.dict(exclude_unset=True))
    return await TweetPydantic.from_tortoise_orm(created_tweet)


@router.get(
    "/{tweet_id}",
    response_model=TweetPydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_tweet(tweet_id: UUID):
    return await TweetPydantic.from_queryset_single(Tweet.get(id=tweet_id))


@router.put(
    "/{tweet_id}",
    response_model=TweetPydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_tweet(tweet_id: UUID, tweet: TweetPydantic):
    await Tweet.filter(id=tweet_id).update(**tweet.dict(exclude_unset=True))
    return await TweetPydantic.from_queryset_single(Tweet.get(id=tweet_id))


@router.delete(
    "/{tweet_id}",
    responses={404: {"model": HTTPNotFoundError}},
)
async def delete_tweet(tweet_id: UUID):
    deleted_count = await Tweet.filter(id=tweet_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Tweet '{tweet_id}' not found")
    return {"message": f"Deleted tweet '{tweet_id}'"}
