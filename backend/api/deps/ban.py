from typing import Callable

from fastapi import HTTPException, Request, status
from redis import asyncio as aioredis


def check_ban(redis: aioredis.Redis, ban_duration: int) -> Callable:
    async def dependency(request: Request):

        ip = request.client.host

        ban_key = f"ban:{ip}"

        if await redis.exists(ban_key):
            ban_expirity = await redis.ttl(ban_key)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "You are banned",
                    "ban_duration_seconds": ban_duration,
                    "time_remaining_seconds": ban_expirity
                }
            )

        return ip

    return dependency

async def ban(ip: str, redis: aioredis.Redis, ban_duration: int) -> None:
    ban_key = f"ban:{ip}"
    await redis.set(ban_key, 1, ex=ban_duration)