import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from redis import asyncio as aioredis

from api.deps.rate_limitting import check_system_rate_limit
from api.routes import prayers

load_dotenv()

app = FastAPI()

GLOBAL_RATE_LIMIT = 50
GLOBAL_TIME_WINDOW = 900
REDIS_URL = os.getenv("REDIS_URL")


@app.middleware("http")
async def global_rate_limit_middleware(request: Request, call_next):
    rate_limit_dependency = check_system_rate_limit(
        global_limit=GLOBAL_RATE_LIMIT,
        time_window=GLOBAL_TIME_WINDOW,
        redis=aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True),
    )

    rate_achieved = await rate_limit_dependency(request)

    if rate_achieved:
        return rate_achieved

    response = await call_next(request)

    return response


app.include_router(prayers.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
