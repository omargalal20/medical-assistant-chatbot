from typing import Annotated

from fastapi import Depends

from business.dependencies import LLMClientDependency
from business.services.orchestrator_service import OrchestratorService


def get_orchestrator(llm_client: LLMClientDependency) -> OrchestratorService:
    """Provide a configured orchestrator."""
    return OrchestratorService(llm_client)


OrchestratorServiceDependency = Annotated[OrchestratorService, Depends(get_orchestrator)]
