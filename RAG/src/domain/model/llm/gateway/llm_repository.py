"File gateway definition"
import abc

class LLMRepository():
    "File repository gateways."
    @abc.abstractmethod
    def __init__(self, config: dict, logger):
        self.logger = logger
        self.config = config

    @abc.abstractmethod
    async def complete(self, prompt):
        """get secret method to be implemented."""
