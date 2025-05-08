from langgraph.prebuilt import create_react_agent
from loguru import logger

from business.clients.llm_client import LLMClient
from business.schemas.fhir_translator_agent import FHIRTranslatorAgentOutput
from business.tools.fhir_tools import FHIRTools
from config.settings import get_settings

settings = get_settings()


class FHIRRetrieverAgent:
    """
    FHIRRetrieverAgent: Retrieves data from a FHIR server based on a translated FHIR query.
    """

    def __init__(
            self,
            llm_client: LLMClient,
            fhir_tools: FHIRTools
    ):
        """
        Initialize FHIRRetrieverAgent configuration.
        """
        self.agent_name = "FHIRRetrieverAgent"
        self.llm = llm_client.get_llm()
        self.fhir_tools = fhir_tools

    async def retrieve(self, fhir_translator_agent_output: FHIRTranslatorAgentOutput):
        """
        Retrieve FHIR resources based on the translated query from the translator agent.
        Input: FHIRTranslatorAgentOutput containing the FHIR query and related metadata.
        Output: FHIR resource data retrieved from the FHIR server.
        """
        logger.info(
            f"{self.agent_name} attempting to retrieve resources using query '{fhir_translator_agent_output.fhir_query}'."
        )

        # Define the system message tailored for FHIR data retrieval
        system_message = (
            "You are a medical assistant specializing in retrieving data from FHIR servers. "
            "Your task is to fetch the required resources based on the provided FHIR query parameters."
        )

        # Construct the agent prompt
        query_prompt = f"""
        # Input
        - FHIR Query: "{fhir_translator_agent_output.fhir_query}"
        - Metadata:
            - Intent: {fhir_translator_agent_output.intent}
            - Entities: {fhir_translator_agent_output.entities}
            - Ambiguities: {fhir_translator_agent_output.ambiguities}
            
        # Tools
        - You have access to the following tools to assist users with retrieving data from FHIR servers:
            - `get_fhir_resources`: Use this tool to fetch specific FHIR resources based on provided query parameters. The tool returns structured data representing the requested FHIR resources.
                - Usage:
                    - {self.fhir_tools.get_fhir_resources_tool.name}
                    - {self.fhir_tools.get_fhir_resources_tool.description}
                    - {self.fhir_tools.get_fhir_resources_tool.args_schema}
        # Knowledge Base
        - You have access to the following detailed information about using the FHIR client to construct and execute resource queries:
            
        ## Searchset Examples
        
        patients.search(birthdate__gt='1944', birthdate__lt='1964')
        - /Patient?birthdate=gt1944&birthdate=lt1964
        
        patients.search(name__contains='John')
        - /Patient?name:contains=John
        
        patients.search(name=['John', 'Rivera'])
        - /Patient?name=John&name=Rivera
        
        patients.search(name='John,Eva')
        - /Patient?name=John,Eva
        
        patients.search(family__exact='Moore')
        - /Patient?family:exact=Moore
        
        patients.search(address_state='TX')
        - /Patient?address-state=TX
        
        patients.search(active=True, _id='id')
        - /Patient?active=true&_id=id
        
        patients.search(gender__not=['male', 'female'])
        - /Patient?gender:not=male&gender:not=female
        
        ## Chained parameters
        patients.search(general_practitioner__Organization__name='Hospital')
        - /Patient?general-practitioner:Organization.name=Hospital
        
        patients.search(general_practitioner__name='Hospital')
        - /Patient?general-practitioner.name=Hospital
        
        Instructions:
        - Use the provided FHIR query parameters to fetch data from the FHIR server.
        - Use the FHIRTools `get_fhir_resources` tool for all retrieval operations.
        - Return the data as a structured JSON response representing the FHIR resources.
        
        - Output Format:
            - Your output should be JSON response representing the FHIR resources.
        """

        # Create the agent with the updated context and retrieval tool
        agent = create_react_agent(
            name=self.agent_name,
            model=self.llm,
            prompt=system_message,
            tools=[self.fhir_tools.get_fhir_resources_tool],
        )

        response = await agent.ainvoke({"messages": query_prompt})
        return response["messages"][-1].content
