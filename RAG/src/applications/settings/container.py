from src.applications.settings.base_settings import GeneralBaseModel
from src.applications.settings.logger import Logger
from src.applications.settings.settings import Config
from src.domain.model.embeddings.gateway.embeddings_repository import EmbeddingsRepository
from src.domain.usecases.generate_answer.generate_answer_use_case import GenerateAnswerUseCase
from src.domain.usecases.retriever.retriever_use_case import GetEmbedingsUseCase
from src.domain.model.llm.gateway.llm_repository import LLMRepository
from src.applications.settings import APP_CONFIG_FILE
from pathlib import Path
from src.infrastructure.helpers.utils import load_json_file
from src.infrastructure.driven_adapters.pg_vector_repository.adapter.pg_vector_repostory import PGVectorRepository
from src.infrastructure.driven_adapters.openia_adapter.adapter.open_ia_adapter import OpenIAAdpater


class SettingsPaths(GeneralBaseModel):
    """Class to manage the paths of the configuration files."""
    CONFIG_PATH: Path

class Container(GeneralBaseModel):
    """Class to manage the dependencies of the application."""
    app_config: Config
    logger: Logger
    generate_answer_use_case: GenerateAnswerUseCase
    get_embeddings_use_case: GetEmbedingsUseCase


def get_deps_container() -> Container:
    """Function to generate the dependencies container of the application."""
    config_paths = SettingsPaths(
        CONFIG_PATH=(APP_CONFIG_FILE),
    )
    app_config_dict = load_json_file(config_paths.CONFIG_PATH)


    app_config = Config(**app_config_dict)
    logger = Logger(app_config.logger)
    logger.info("Configs load successfully.")

    llm_repository = OpenIAAdpater(config=app_config, logger=logger)
    generate_answer_use_case = GenerateAnswerUseCase(
        config=app_config,
        logger=logger,
        llm_repository=llm_repository
    )

    embeddings_repository = PGVectorRepository(config=app_config, logger=logger)
    get_embeddings_use_case = GetEmbedingsUseCase(
        config=app_config,
        logger=logger,
        embeddings_repository=embeddings_repository
    )

    logger.info("Generate the dependencies container successfully.")
    return Container(
            app_config=app_config,
            logger=logger,
            generate_answer_use_case=generate_answer_use_case,
            get_embeddings_use_case=get_embeddings_use_case
    )
