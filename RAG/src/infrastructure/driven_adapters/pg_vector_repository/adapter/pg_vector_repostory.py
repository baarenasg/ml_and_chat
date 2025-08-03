from src.domain.model.embeddings.gateway.embeddings_repository import EmbeddingsRepository
from sqlalchemy import make_url
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever

class PGVectorRepository(EmbeddingsRepository):
    "File repository for PGVector."

    def __init__(self, config: dict, logger):
        super().__init__(config, logger)
        self.config = config
        self.logger = logger
        # Initialize the PGVectorStore with the provided configuration

        url = make_url(self.config.postgresql.connection_string)

        self.vector_store = PGVectorStore.from_params(
            host=url.host,
            port=url.port,
            user=url.username,
            password=url.password,
            database=config.postgresql.database,
            table_name=self.config.postgresql.table_name,
            embed_dim=self.config.postgresql.embed_dim,
            hnsw_kwargs=self.config.postgresql.hnsw_kwargs
        )

        index = VectorStoreIndex.from_vector_store(vector_store=self.vector_store)
        self.retriever = index.as_retriever(similarity_top_k=5)

        self.retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=self.config.retriever.k    ,
        )


    async def get_embeddings(self, question: str):
        nodes = self.retriever.retrieve(question)
        context_str = "\n\n".join([node.node.get_content() for node in nodes])
        self.logger.info(f"Retrieved context for question: '{question}': {context_str}")
        return context_str