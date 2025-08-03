import uuid
import logging
from typing import Any, Dict, Optional, Union

from pydantic import (AliasChoices,
                      Field,
                      ValidationInfo,
                      field_validator)

from src.applications.settings.base_settings import (GeneralBaseModel,
                                                     GeneralBaseSettings)


class LoggerConfig(GeneralBaseSettings):
    """Class to manage the logger configuration of the application."""
    LOGGER_FORMAT: str = "%(asctime)s - %(message)s"
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    LOG_LEVEL: Optional[Union[str, int]] = logging.INFO
    LOG_NAME: str = "uvicorn.access"

    LOGGER_DATE_FORMAT: str = Field("", validate_default=True)

    @field_validator("LOGGER_DATE_FORMAT", mode="before", check_fields=True)
    @classmethod
    def build_logger_date_format(cls, _: str, info: ValidationInfo) -> str:
        """Build the logger date format."""
        return "[" + info.data.get("DATE_FORMAT") + "]"


class OpenAiConfig(GeneralBaseSettings):
    """Class to manage the OpenAI configuration of the application."""

    api_key: str = Field(
        "OPENAI_API_KEY",
        alias='OPENAI_API_KEY',
        validation_alias=AliasChoices("OPENAI_API_KEY", "OPENAI_API_KEY")
    )

class PostgreSqlConfig(GeneralBaseSettings):
    """Class to manage the PostgreSQL configuration of the application."""
    connection_string: str = Field(
        "postgresql://postgres-user:postgres-pass@localhost:5432",
        alias='PG_CONNECTION_STRING',
        validation_alias=AliasChoices("PG_CONNECTION_STRING", "PG_CONNECTION_STRING")
    )
    database: str = "vector_bd_movies"
    table_name: str = "movies"
    embed_dim: int = 1536 
    hnsw_kwargs: Dict[str, Any] = {
        "hnsw_m": 16,
        "hnsw_ef_construction": 64,
        "hnsw_ef_search": 40,
        "hnsw_dist_method": "vector_cosine_ops",
    }

class RetrieverConfig(GeneralBaseModel):
    """Class to manage the retriever configuration of the application."""
    k: int = 5

class Config(GeneralBaseSettings):
    """Class to manage the configuration of the application."""
    url_prefix: str
    logger: LoggerConfig = Field(default_factory=LoggerConfig)
    postgresql: PostgreSqlConfig
    openai: OpenAiConfig
    retriever: RetrieverConfig

