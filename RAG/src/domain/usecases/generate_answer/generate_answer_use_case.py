"""Download file use case module."""
from src.domain.model.llm.gateway.llm_repository import LLMRepository
from src.domain.model.message_error.gateways.message_error_repository \
    import MessageErrorRepository
from src.domain.model.answer.answer_model import Answer, Message


class GenerateAnswerUseCase():
    def __init__(self, config: dict, logger, llm_repository: LLMRepository):
        self.config = config
        self.logger = logger
        self.llm_repository = llm_repository

    template_str = """Hemos proporcionado la siguiente información de contexto.
        ---------------------
        {{ context_str }}
        ---------------------
        Dada esta información, por favor responde la siguiente pregunta: {{ query_str }}
        Responde de manera concisa y directa, utilizando la información proporcionada en el contexto.
        Si no hay información relevante en el contexto, responde con "No tengo información sobre eso".
        Si la pregunta no es clara, responde con "Pregunta no clara".
        Si la pregunta es sobre una película, responde con el título de la película y su imagen al final para que se muestre bien en la interfaz de usuario.
        Si la intención de la pregunta es un saludo di que eres un asistente virtual y sabes sobre peliculas de los 80'
        """
    async def generate_answer(self, context_str: str, query_str: str,model: str ) -> str:
        """
        Generate an answer based on the context and query strings.
        """
        prompt = self.template_str.replace("{{ context_str }}", context_str).replace("{{ query_str }}", query_str)
        self.logger.info(f"Generated prompt: {prompt}")
        
        try:
            conent = await self.llm_repository.complete(prompt,model)
            answer = Answer(
                message=Message(
                    role="assistant",
                    content=conent
                )
            )
            self.logger.info(f"Generated answer: {answer}")
            return answer
        except MessageErrorRepository as error:
            self.logger.error(f"Error generating the answer: {error}")
            raise error
        