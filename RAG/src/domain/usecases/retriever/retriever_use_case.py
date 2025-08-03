"""Download file use case module."""
from src.domain.model.embeddings.gateway.embeddings_repository import EmbeddingsRepository
from src.domain.model.message_error.gateways.message_error_repository \
    import MessageErrorRepository

class GetEmbedingsUseCase():
    """Download file use case."""
    def __init__(self, config: dict, logger, embeddings_repository: EmbeddingsRepository):
        self.config = config
        self.logger = logger
        self.embeddings_repository = embeddings_repository


    async def get_embeddings(self, question: str):
        """Get the embeddings for the indicated document."""
        try:
            doocuments = await self.embeddings_repository.get_embeddings(question)
            return doocuments
        except MessageErrorRepository as error:
            self.logger.error(f"Error getting the embeddings: {error}")