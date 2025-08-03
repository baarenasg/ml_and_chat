"File gateway definition"
import abc

class EmbeddingsRepository():
    "File repository gateways."
    @abc.abstractmethod
    def __init__(self, config: dict, logger):
        self.logger = logger
        self.config = config

    @abc.abstractmethod
    async def get_embeddings(self, question):
        """get secret method to be implemented."""
