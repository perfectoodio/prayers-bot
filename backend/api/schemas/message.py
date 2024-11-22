from pydantic import BaseModel


class UserMessage(BaseModel):
    user_message: str

    class Config:
        from_attributes = True

