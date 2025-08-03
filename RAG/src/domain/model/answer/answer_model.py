from typing import List
from pydantic import BaseModel

class Message(BaseModel):
    """Output aio model."""
    role: str = "assistant"
    content: str

class Answer(BaseModel):
    """Input aio model."""
    message: Message

