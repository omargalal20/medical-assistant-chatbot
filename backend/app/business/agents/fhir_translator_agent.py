from langgraph.prebuilt import create_react_agent
from loguru import logger

from business.clients.llm_client import LLMClient
from business.schemas.fhir_translator_agent import FHIRTranslatorAgentOutput
from config.settings import get_settings
from presentation.schemas.medical_qa_assistant import DoctorQuery

settings = get_settings()


class FHIRTranslatorAgent:
    """
    FHIRTranslatorAgent
    """

    def __init__(
            self,
            llm_client: LLMClient,
    ):
        """
        Initialize FHIRTranslatorAgent configuration.
        """

        self.agent_name = "FHIRTranslatorAgent"
        self.llm = llm_client.get_llm()

    async def translate(self, patient_id: str, doctor_query: DoctorQuery) -> FHIRTranslatorAgentOutput:
        """
        Translate
        \nInput: Doctor’s natural-language query
        \nOutput: FHIR-compliant API query (e.g., RESTful URL + params)
        """
        logger.info(f"{self.agent_name} attempting to translate '{doctor_query}' to FHIR-compliant API query.")

        # Define the system message tailored for FHIR query translation
        system_message = (
            "You are a precise and efficient assistant that translates natural-language medical queries into FHIR-compliant API queries. "
            "Your output should be concise and structured as a valid FHIR RESTful query URL with parameters."
        )

        # Example prompt for the agent
        query = f"""
        - Doctor's query: "{doctor_query.content}"
        - Metadata:
            - Patient ID: {patient_id}
            - Query Date: {doctor_query.created_at.isoformat()}
        - Use the following for your thought process:
            - Use the following details:
                1. **Intent**: Identify the primary goal of the query (e.g., retrieve patient data, analyze observations, list medications).
                2. **Entities**: Extract key entities such as:
                    - Resource type (e.g., Observation, Patient, MedicationRequest)
                    - Relevant parameters (e.g., patient name, date range, observation type)
                3. **Ambiguities**: Identify any missing or unclear details in the query.
                4. **Clarifications**: Formulate questions to address ambiguities or missing details.

            - Use the intent, entities, ambiguities, and clarifications to translate the query into a FHIR API query parameters format, such as:
                ?patient=564b051c-6fcf-4123-909e-5ee74d5f6a9a&authoredon=ge2025-02-07&status=active,completed

            - If ambiguities exist, determine which tools are needed to clarify them:
                **Ambiguities**:
                - Missing patient name.
                - Unclear date range.

                **Suggested Clarifications**:
                - "Which patient's data should be retrieved?"
                - "What time frame should the query cover?"
        - Output Format:
            - Your output should only be the valid FHIR query parameters without any server URL or additional text.
        """

        # Create the agent with the updated context
        agent = create_react_agent(name=self.agent_name, model=self.llm, prompt=system_message, tools=[],
                                   response_format=FHIRTranslatorAgentOutput)

        response = await agent.ainvoke({"messages": query})
        logger.info(f"Structured Response: {response["structured_response"]}")
        return response["structured_response"]
