from typing import Any

from langgraph.prebuilt import create_react_agent
from loguru import logger

from business.clients.llm_client import LLMClient
from business.schemas.fhir_translator_agent import FHIRTranslatorAgentOutput
from config.settings import get_settings

settings = get_settings()


class FHIRFormatterAgent:
    """
    FHIRFormatterAgent
    """

    def __init__(
            self,
            llm_client: LLMClient,
    ):
        """
        Initialize FHIRFormatterAgent configuration.
        """
        self.agent_name = "FHIRFormatterAgent"
        self.llm = llm_client.get_llm()

    async def format(self, fhir_translator_agent_output: FHIRTranslatorAgentOutput,
                     fhir_retriever_agent_output: Any):
        """
        Format
        \nInput: Retrieved raw FHIR data and the doctor’s original natural-language query.
        \nOutput: Natural language summary of the FHIR data suitable for LLM consumption.
        """
        logger.info(
            f"{self.agent_name} is converting raw FHIR data into an LLM-friendly format by extracting key details and presenting them concisely."
        )

        # Define the system message tailored for FHIR data formatting
        system_message = (
            "You are a medical assistant specializing in summarizing patient data retrieved from FHIR servers. "
            "Your task is to convert raw FHIR data into a concise, human-readable format, preserving key details."
        )

        # Construct the agent prompt
        query_prompt = f"""
        # Input
        - {fhir_retriever_agent_output}
            
        # Context
        - FHIR Query: "{fhir_translator_agent_output.fhir_query}"
        - Metadata:
            - Intent: {fhir_translator_agent_output.intent}
            - Entities: {fhir_translator_agent_output.entities}
            - Ambiguities: {fhir_translator_agent_output.ambiguities}

        Instructions:
        - Extract and summarize the most relevant details from the retrieved FHIR data.
        - Provide a clear, structured summary in natural language, tailored to the doctor's query.
        - Ensure the summary is concise but includes essential details like encounter dates, types, locations, clinicians, and other critical metadata.
        - Handle missing or incomplete data gracefully, and clearly indicate any limitations or gaps in the retrieved data.

        Output Format:
        - A natural-language summary of the FHIR data in paragraph or bullet-point form.
        """

        # Create the agent with the updated context and retrieval tool
        agent = create_react_agent(
            name=self.agent_name,
            model=self.llm,
            prompt=system_message,
            tools=[],
        )
        response = await agent.ainvoke({"messages": query_prompt})
        return response["messages"][-1].content
