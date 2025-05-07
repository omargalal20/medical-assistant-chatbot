from typing import Annotated

from fastapi import Depends
from fhirpy import AsyncFHIRClient

from business.agents.fhir_translator_agent import FHIRTranslatorAgent
from business.clients.fhir_client import fhir_client
from business.clients.llm_client import LLMClient
from business.clients.retriever_client import RetrieverClient


def get_llm_client() -> LLMClient:
    return LLMClient()


LLMClientDependency = Annotated[LLMClient, Depends(get_llm_client)]


def get_retriever_client() -> RetrieverClient:
    return RetrieverClient()


RetrieverClientDependency = Annotated[RetrieverClient, Depends(get_retriever_client)]


def get_fhir_server() -> AsyncFHIRClient:
    return fhir_client.get_fhir_server()


FHIRServerDependency = Annotated[AsyncFHIRClient, Depends(get_fhir_server)]


def get_fhir_translator_agent(
        llm_client: LLMClientDependency) -> FHIRTranslatorAgent:
    """
    Creates and returns an instance of the TranslatorAgent.

    The TranslatorAgent is responsible for converting natural-language queries
    into FHIR-compliant API queries using the provided LLM and LangSmith clients.
    """
    return FHIRTranslatorAgent(llm_client)


TranslatorAgentDependency = Annotated[FHIRTranslatorAgent, Depends(get_fhir_translator_agent)]
