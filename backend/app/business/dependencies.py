from typing import Annotated

from fastapi import Depends

from business.clients.llm_client import LLMClient
from business.clients.retriever_client import RetrieverClient


def get_llm_client() -> LLMClient:
    return LLMClient()


def get_retriever_client() -> RetrieverClient:
    return RetrieverClient()


LLMClientDependency = Annotated[LLMClient, Depends(get_llm_client)]
RetrieverClientDependency = Annotated[RetrieverClient, Depends(get_retriever_client)]
