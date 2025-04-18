from typing import Annotated

from fastapi import Depends

from business.dependencies import LLMClientDependency, RetrieverClientDependency
from business.services.orchestrator_service import OrchestratorService


def get_orchestrator(llm_client: LLMClientDependency,
                     retriever_client: RetrieverClientDependency) -> OrchestratorService:
    """Provide a configured orchestrator."""
    return OrchestratorService(llm_client, retriever_client)


OrchestratorServiceDependency = Annotated[OrchestratorService, Depends(get_orchestrator)]
