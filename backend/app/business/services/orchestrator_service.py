from datetime import datetime
from typing import AsyncIterable

from langchain_core.exceptions import LangChainException
from langchain_core.output_parsers import StrOutputParser
from loguru import logger

from business.clients.llm_client import LLMClient
from business.schemas.medical_qa_assistant import AssistantResponse
from business.templates.v1.medical_qa_template import get_medical_qa_template
from data.models.enums.role import Role
from presentation.schemas.medical_qa_assistant import DoctorQuery


class OrchestratorService:
    """
    OrchestratorService that is responsible for connecting the LLM to external services
    """

    def __init__(self, llm_client: LLMClient):
        """Initialize with injected service dependencies."""
        self.llm_client = llm_client
        self.llm = llm_client.get_llm()
        self.template = get_medical_qa_template("medical_qa")

    async def chat(self, doctor_query: DoctorQuery) -> AssistantResponse:
        """
        Generate a complete, evidence-based response for a medical query.

        This function:
        - Constructs a query-specific input template based on the doctor's question.
        - Runs a pre-configured chain combining the template, LLM, and output parser.
        - Returns the generated response as an `LLMResponse` object.

        Parameters:
        - doctor_query (str): The medical question or prompt provided by the doctor.

        Returns:
        - LLMResponse: Contains the generated response in structured format.

        Raises:
        - RuntimeError: If the chain fails to generate a response due to an exception.
        """

        logger.info(f"OrchestratorService, chat, doctor_query: {doctor_query}")

        template = get_medical_qa_template("medical_qa")

        template_vars = {
            "doctor_query": doctor_query.content
        }

        logger.debug(f"Medical QA Template Variables: {template_vars}")

        # Create a runnable sequence
        chain = template | self.llm | StrOutputParser()

        try:
            response = await chain.ainvoke(template_vars)

            logger.debug(f"Response: {response}")

            current_time = datetime.now()

            return AssistantResponse(
                id=current_time,
                role=Role.ASSISTANT,
                content=response,
                created_at=current_time
            )
        except LangChainException as e:
            logger.error(f"LLM failed to generate response: {str(e)}")
            raise RuntimeError("LLM failed to generate response.") from e

    async def chat_stream(self, doctor_query: str) -> AsyncIterable[str]:
        """
        Stream a response for a medical query in real-time.

        This function:
        - Uses an async generator to provide incremental updates to the response.
        - Constructs a query-specific input template based on the doctor's question.
        - Streams responses from the LLM, yielding formatted data chunks as they are generated.

        Parameters:
        - doctor_query (str): The medical question or prompt provided by the doctor.

        Yields:
        - str: Formatted chunks of the response, each encapsulated as an event stream data message.

        Raises:
        - RuntimeError: If the chain fails to stream a response due to an exception.
        """

        template = get_medical_qa_template("medical_qa")

        template_vars = {
            "doctor_query": doctor_query
        }

        logger.debug(f"Medical QA Template Variables for Streaming: {template_vars}")

        # Assuming `self.llm` supports streaming via an async generator
        chain = template | self.llm | StrOutputParser()

        try:
            async for chunk in chain.astream(template_vars):
                content = chunk.replace("\n", "<br>")
                logger.debug(f"Streamed content: {content}")
                yield f"data: {content}\n\n"
        except LangChainException as e:
            logger.error(f"LLM streaming failed: {str(e)}")
            raise RuntimeError("LLM streaming failed.") from e
