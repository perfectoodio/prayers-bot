import os

from fastapi import APIRouter, Depends, HTTPException, status
from redis import asyncio as aioredis

from api.deps.ban import ban, check_ban
from api.deps.rate_limitting import check_user_rate_limit
from api.schemas.message import UserMessage
from assistant.assistant import send_message
from twitter.tweet import create_tweet

router = APIRouter()

RATE_LIMIT = 5
TIME_WINDOW = 600
BAN_DURATION = 7 * 24 * 60 * 60
REDIS_URL = os.getenv("REDIS_URL")

redis = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)


@router.post("/prayers", status_code=status.HTTP_201_CREATED)
async def post_prayer(
    message: UserMessage,
    ip: str = Depends(
        check_user_rate_limit(rate_limit=RATE_LIMIT, time_window=TIME_WINDOW, redis=redis)
    ),
    banned_ip: str = Depends(check_ban(redis=redis, ban_duration=BAN_DURATION)),
):
    validation = await send_message(message.user_message)

    if validation["isSensitive"] or not validation["isPrayerRequest"]:
        if validation["isSensitive"]:
            await ban(banned_ip, redis, BAN_DURATION)

        raise HTTPException(status_code=400, detail=validation)

    try:
        create_tweet(message.user_message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"detail": f"Prayer tweeted sucessfully: {message.user_message}"}
