import abc
from src.domain.model.question.question_model import Question


class QuestionRepository(abc.ABC):
    """Input repository gateways."""

    @abc.abstractmethod
    async def get_question(self, ta_config, event_aio) -> Question:
        """Generate a question."""
