from typing import Annotated

from fastapi import Depends
from fhirclient.server import FHIRServer

from business.clients.fhir_client import fhir_client_interface
from business.clients.llm_client import LLMClient
from business.clients.retriever_client import RetrieverClient


def get_llm_client() -> LLMClient:
    return LLMClient()


def get_retriever_client() -> RetrieverClient:
    return RetrieverClient()


def get_fhir_server() -> FHIRServer:
    return fhir_client_interface.get_fhir_server()


LLMClientDependency = Annotated[LLMClient, Depends(get_llm_client)]
RetrieverClientDependency = Annotated[RetrieverClient, Depends(get_retriever_client)]
FHIRServerDependency = Annotated[FHIRServer, Depends(get_fhir_server)]
