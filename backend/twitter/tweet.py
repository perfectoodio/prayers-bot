import asyncio
import os

from dotenv import load_dotenv
from tweepy.asynchronous import AsyncClient

load_dotenv()


app = AsyncClient(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
)


async def create_tweet(message):
    await app.create_tweet(
        text=message
    )

    return {"user_message": message}

if __name__ == "__main__":
    print(asyncio.run(create_tweet("Teste")))