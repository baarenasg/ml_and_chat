"file model definition"
from pydantic import BaseModel

class Answer(BaseModel):
    """
    File model.
    Attributes:
        file_name (str): The name of the file.
        file_path (str): The path to the file.
    """
    answer: str