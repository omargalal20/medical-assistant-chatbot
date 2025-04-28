from typing import Annotated

from fastapi import Depends
from fhirpy import AsyncFHIRClient

from business.clients.fhir_client import fhir_client
from business.clients.llm_client import LLMClient
from business.clients.retriever_client import RetrieverClient


def get_llm_client() -> LLMClient:
    return LLMClient()


def get_retriever_client() -> RetrieverClient:
    return RetrieverClient()


def get_fhir_server() -> AsyncFHIRClient:
    return fhir_client.get_fhir_server()


LLMClientDependency = Annotated[LLMClient, Depends(get_llm_client)]
RetrieverClientDependency = Annotated[RetrieverClient, Depends(get_retriever_client)]
FHIRServerDependency = Annotated[AsyncFHIRClient, Depends(get_fhir_server)]
