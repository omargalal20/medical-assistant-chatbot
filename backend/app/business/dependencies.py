from typing import Annotated

from fastapi import Depends
from fhirpy import AsyncFHIRClient

from business.agents.fhir_formatter_agent import FHIRFormatterAgent
from business.agents.fhir_retriever_agent import FHIRRetrieverAgent
from business.agents.fhir_translator_agent import FHIRTranslatorAgent
from business.clients.fhir_client import fhir_client
from business.clients.llm_client import LLMClient
from business.clients.pubmed_retriever_client import PubmedRetrieverClient
from business.tools.fhir_tools import FHIRTools


def get_llm_client() -> LLMClient:
    return LLMClient()


LLMClientDependency = Annotated[LLMClient, Depends(get_llm_client)]


def get_retriever_client() -> PubmedRetrieverClient:
    return PubmedRetrieverClient()


RetrieverClientDependency = Annotated[PubmedRetrieverClient, Depends(get_retriever_client)]


def get_fhir_server() -> AsyncFHIRClient:
    return fhir_client.get_fhir_server()


FHIRServerDependency = Annotated[AsyncFHIRClient, Depends(get_fhir_server)]


def get_fhir_tools(fhir_server: FHIRServerDependency) -> FHIRTools:
    return FHIRTools(fhir_server)


FHIRToolsDependency = Annotated[FHIRTools, Depends(get_fhir_tools)]


def get_fhir_translator_agent(
        llm_client: LLMClientDependency) -> FHIRTranslatorAgent:
    """
    Creates and returns an instance of the TranslatorAgent.

    The TranslatorAgent is responsible for converting natural-language queries
    into FHIR-compliant API queries using the provided LLM and LangSmith clients.
    """
    return FHIRTranslatorAgent(llm_client)


TranslatorAgentDependency = Annotated[FHIRTranslatorAgent, Depends(get_fhir_translator_agent)]


def get_fhir_retriever_agent(
        llm_client: LLMClientDependency,
        fhir_server: FHIRServerDependency
) -> FHIRRetrieverAgent:
    """
    Creates and returns an instance of the TranslatorAgent.

    The TranslatorAgent is responsible for converting natural-language queries
    into FHIR-compliant API queries using the provided LLM and LangSmith clients.
    """
    fhir_tools = get_fhir_tools(fhir_server)
    return FHIRRetrieverAgent(llm_client, fhir_tools)


FHIRRetrieverAgentDependency = Annotated[FHIRRetrieverAgent, Depends(get_fhir_retriever_agent)]


def get_fhir_formatter_agent(
        llm_client: LLMClientDependency) -> FHIRFormatterAgent:
    """
    Creates and returns an instance of the FHIRFormatterAgent.

    The FHIRFormatterAgent is responsible for converting raw FHIR data into an
    LLM-friendly format by extracting key details and structuring them concisely.
    """
    return FHIRFormatterAgent(llm_client)


FHIRFormatterAgentDependency = Annotated[FHIRFormatterAgent, Depends(get_fhir_formatter_agent)]
