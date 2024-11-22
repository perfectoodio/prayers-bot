import os

from dotenv import load_dotenv
from tweety import Twitter

load_dotenv()


app = Twitter("session")


def login():
    if os.path.exists("session.tw_session"):
        app.connect()
    else:
        app.sign_in(
            username=os.getenv("TWITTER_USERNAME"),
            password=os.getenv("TWITTER_PASSWORD"),
        )
    return "Login successful"


def create_tweet(message):
    login()
    app.create_tweet(message)
    return {"user_message": message}