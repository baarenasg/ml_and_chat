from typing import List
from pydantic import BaseModel


class Question(BaseModel):
    """Input aio model."""
    model: str
    messages: List
    stream: bool