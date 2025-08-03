from src.domain.model.llm.gateway.llm_repository import LLMRepository
from llama_index.llms.openai import OpenAI


class OpenIAAdpater(LLMRepository):
    """
    OpenIAAdapter class that implements the LLMRepository interface.
    This class is responsible for interacting with the OpenAI API.
    """

    def __init__(self, config: dict, logger):
        super().__init__(config, logger)
        self.logger = logger
        self.config = config

    async def complete(self, prompt: str, model:str) -> str:
        """
        Method to complete a query using the OpenAI API.
        """

        self.logger.info(f"Completing prompt: {prompt} with model: {model}")
        llm = OpenAI(model=model)
        response = llm.complete(prompt)
        self.logger.info(f"Response from OpenAI: {response}")
        return response.text