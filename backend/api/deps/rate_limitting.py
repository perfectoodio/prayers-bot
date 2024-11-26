from typing import Callable

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from redis import asyncio as aioredis


def check_user_rate_limit(
    rate_limit: int, time_window: int, redis: aioredis.Redis
) -> Callable:
    async def dependency(request: Request):
        ip = request.client.host

        rate_key = f"rate_limit:{ip}"

        current_count = await redis.get(rate_key)

        if current_count:
            if int(current_count) >= rate_limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "type": "error",
                        "reason": "User rate limit exceeded",
                        "limit": rate_limit,
                        "time_window_seconds": time_window,
                        "retry_after_seconds": await redis.ttl(rate_key),
                    },
                )

            await redis.incr(rate_key)

        else:
            await redis.set(rate_key, 1, ex=time_window)

        return ip

    return dependency


def check_system_rate_limit(
    global_limit: int, time_window: int, redis: aioredis.Redis
) -> Callable:
    async def dependency(request: Request):

        rate_key = "system_rate_limit"

        current_count = await redis.get(rate_key)

        if current_count:
            if int(current_count) >= global_limit:

                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": {
                            "type": "error",
                            "reason": "System rate limit exceeded",
                            "limit": global_limit,
                            "time_window_seconds": time_window,
                            "retry_after_seconds": await redis.ttl(rate_key),
                        }
                    },
                )

            await redis.incr(rate_key)

        else:
            await redis.set(rate_key, 1, ex=time_window)

        return None

    return dependency
