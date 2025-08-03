from typing import Annotated
from fastapi import APIRouter, Depends, Request, BackgroundTasks
from src.domain.usecases.generate_answer.generate_answer_use_case import GenerateAnswerUseCase
from src.domain.usecases.retriever.retriever_use_case import GetEmbedingsUseCase
from src.infrastructure.entry_points.fast_api.handlers.rag_handler import RagHandler
from src.applications.settings.container import Container
router = APIRouter()

def get_generate_answer_use_case(request: Request):
    """Get create_user use case."""
    container: "Container" = request.app.container
    return container.generate_answer_use_case


def get_get_embeddings_use_case(request: Request):
    """Get create_user use case."""
    container: "Container" = request.app.container
    return container.get_embeddings_use_case

GenerateAnswerUseCaseDep = Annotated[GenerateAnswerUseCase,
                                      Depends(get_generate_answer_use_case)]
GetEmbeddingsUseCaseDep = Annotated[GetEmbedingsUseCase,
                                     Depends(get_get_embeddings_use_case)]

@router.post("/chat", tags=["async"])
async def handle_chat(
        request: Request,
        generate_answer_use_case: GenerateAnswerUseCaseDep,
        get_embeddings_use_case: GetEmbeddingsUseCaseDep,
        ):

    handler = RagHandler(request,
                         generate_answer_use_case,
                         get_embeddings_use_case)
    return await handler.process()