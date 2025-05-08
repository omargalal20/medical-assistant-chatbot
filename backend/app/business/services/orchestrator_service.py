from datetime import datetime
from typing import AsyncIterable

from langchain_community.tools import PubmedQueryRun
from langchain_core.documents import Document
from langchain_core.exceptions import LangChainException
from langchain_core.output_parsers import StrOutputParser
from loguru import logger

from business.agents.fhir_formatter_agent import FHIRFormatterAgent
from business.agents.fhir_retriever_agent import FHIRRetrieverAgent
from business.agents.fhir_translator_agent import FHIRTranslatorAgent
from business.clients.llm_client import LLMClient
from business.clients.retriever_client import RetrieverClient
from business.schemas.fhir_translator_agent import FHIRTranslatorAgentOutput
from business.schemas.medical_qa_assistant import AssistantResponse
from business.templates.v2.medical_qa_template import get_medical_qa_template
from business.templates.v2.patient_qa_template import get_patient_qa_template
from data.models.enums.role import Role
from presentation.schemas.medical_qa_assistant import DoctorQuery


class OrchestratorService:
    """
    OrchestratorService that is responsible for connecting the LLM to external services
    """

    def __init__(self,
                 llm_client: LLMClient,
                 retriever_client: RetrieverClient,
                 fhir_translator_agent: FHIRTranslatorAgent,
                 fhir_retriever_agent: FHIRRetrieverAgent,
                 fhir_formatter_agent: FHIRFormatterAgent
                 ):
        """Initialize with injected service dependencies."""
        self.llm_client = llm_client
        llm_client.bind_tools_to_llm([PubmedQueryRun()])
        self.llm = llm_client.get_llm()
        self.template = get_medical_qa_template("medical_qa")
        self.retriever = retriever_client
        self.fhir_translator_agent = fhir_translator_agent
        self.fhir_retriever_agent = fhir_retriever_agent
        self.fhir_formatter_agent = fhir_formatter_agent

    async def general_medical_qa_chat(self, doctor_query: DoctorQuery) -> AssistantResponse:
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

        # Retrieval
        relevant_articles: list[Document] = await self.retriever.get_relevant_documents(doctor_query.content)

        logger.debug(relevant_articles)

        # Augmentation
        template = get_medical_qa_template("medical_qa")

        template_vars = {
            "doctor_query": doctor_query.content
        }

        if not relevant_articles or (len(relevant_articles) == 0):
            logger.warning("No relevant articles retrieved. Proceeding without evidence.")
            template_vars["context"] = "No relevant articles found."
        else:
            template_vars["context"] = "\n\n".join(
                [
                    f"PubMed ID: {doc.metadata.get('uid', 'Unknown')} | Title: {doc.metadata.get('Title', 'Unknown')} | Published: {doc.metadata.get('Published', 'Unknown')} | Content: {doc.page_content}"
                    for doc in
                    relevant_articles]
            )

        logger.debug(f"Medical QA Template Variables: {template_vars}")

        # Generation
        response = await self.llm_client.generate_response(template, template_vars)

        logger.debug(f"Response: {response}")

        current_time = datetime.now()

        return AssistantResponse(
            id=current_time,
            role=Role.ASSISTANT,
            content=response,
            created_at=current_time
        )

    async def general_medical_qa_chat_stream(self, doctor_query: DoctorQuery) -> AsyncIterable[str]:
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

        logger.info(f"OrchestratorService, chat_stream, doctor_query: {doctor_query}")

        relevant_articles = await self.retriever.get_relevant_documents(doctor_query.content)

        logger.debug(relevant_articles)

        template = get_medical_qa_template("medical_qa")

        template_vars = {
            "doctor_query": doctor_query.content
        }

        logger.debug(f"Medical QA Template Variables: {template_vars}")

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

    async def patient_medical_qa_chat(self, doctor_query: DoctorQuery) -> AssistantResponse:
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

        logger.info(f"{self.__class__.__name__}, patient_medical_qa_chat, doctor_query: {doctor_query}")

        """
        Translator Agent
        • Input: Doctor’s natural-language query
        • Output: FHIR-compliant API query (e.g. RESTful URL + params)
        """

        try:
            fhir_translator_agent_output: FHIRTranslatorAgentOutput = await self.fhir_translator_agent.translate(
                doctor_query)
        except Exception as e:
            logger.error(f"Error during ResearchGate lookup: {e}")
            raise

        logger.info(f"FHIRTranslatorAgentOutput: {fhir_translator_agent_output}")

        """
        Retriever Agent
        • Input: FHIR query
        • Action: Calls the FHIR server, handles paging, authentication, retries
        • Output: Raw FHIR JSON bundle
        """

        try:
            fhir_retriever_agent_output = await self.fhir_retriever_agent.retrieve(fhir_translator_agent_output)
        except Exception as e:
            logger.error(f"Error during ResearchGate lookup: {e}")
            raise

        logger.info(f"FHIRRetrieverAgentOutput: {fhir_retriever_agent_output}")

        """
        Formatter Agent
        • Input: FHIR JSON bundle
        • Action: Extracts relevant fields, summarizes or normalizes them
        • Output: Structured, concise text or JSON payload ready for the LLM
        """

        try:
            fhir_formatter_agent_output = await self.fhir_formatter_agent.format(fhir_translator_agent_output,
                                                                                 fhir_retriever_agent_output)
        except Exception as e:
            logger.error(f"Error during ResearchGate lookup: {e}")
            raise

        logger.info(f"FHIRFormatterAgentOutput: {fhir_formatter_agent_output}")

        """
        LLM Invocation
        • Input: Original doctor query + formatted patient data
        • Output: Final answer to the doctor
        """

        # Augmentation
        template = get_patient_qa_template("patient_qa")

        template_vars = {
            "doctor_query": doctor_query.content,
            "fhir_query": fhir_translator_agent_output.fhir_query,
            "intent": fhir_translator_agent_output.intent,
            "entities": fhir_translator_agent_output.entities,
            "ambiguities": fhir_translator_agent_output.ambiguities,
            "formatted_fhir_data": fhir_formatter_agent_output
        }

        # Generation
        response = await self.llm_client.generate_response(template, template_vars)

        logger.debug(f"Response: {response}")

        current_time = datetime.now()

        return AssistantResponse(
            id=current_time,
            role=Role.ASSISTANT,
            content=response,
            created_at=current_time
        )
