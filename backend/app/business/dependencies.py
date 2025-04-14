from typing import Annotated

from fastapi import Depends

from business.clients.llm_client import LLMClient


def get_llm_client() -> LLMClient:
    return LLMClient()


LLMClientDependency = Annotated[LLMClient, Depends(get_llm_client)]
