
from fastapi import Request, BackgroundTasks, HTTPException
from src.domain.usecases.generate_answer.generate_answer_use_case import GenerateAnswerUseCase
from src.domain.usecases.retriever.retriever_use_case import GetEmbedingsUseCase
from src.applications.settings.container import Container
from src.domain.model.question.question_model import Question
from pydantic import ValidationError

class RagHandler():
    """Process aio use case."""
    def __init__(self,
                request: Request,
                generate_answer_use_case: GenerateAnswerUseCase,
                get_embeddings_use_case: GetEmbedingsUseCase,
                ):
        

        self.container: "Container" = request.app.container
        self.logger = self.container.logger
        self.request = request
        self.get_embeddings_use_case = get_embeddings_use_case
        self.generate_answer_use_case = generate_answer_use_case

    async def process(self) :
        """Process aio."""
        body = await self._get_body()
        self.logger.info(f"Processing request with body: {body}")
        question = body.messages[-1]["content"]
        self.logger.info(f"Extracted question: {question}")
        context_str = await self.get_embeddings_use_case.get_embeddings(question)
        answer = await self.generate_answer_use_case.generate_answer(
            context_str=context_str,
            query_str=question,
            model=body.model 
        )
        return  answer

    async def _get_body(self) -> Question:
        try:
            body = await self.request.json()
 
            return Question(**body)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors()) from e
