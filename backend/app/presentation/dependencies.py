from typing import Annotated

from fastapi import Depends

from business.dependencies import LLMClientDependency, RetrieverClientDependency, FHIRServerDependency
from business.services.orchestrator_service import OrchestratorService
from business.services.patients_service import PatientsService


def get_orchestrator(llm_client: LLMClientDependency,
                     retriever_client: RetrieverClientDependency) -> OrchestratorService:
    """Provide a configured orchestrator."""
    return OrchestratorService(llm_client, retriever_client)


def get_patients_service(
        fhir_server: FHIRServerDependency
) -> PatientsService:
    return PatientsService(fhir_server)


OrchestratorServiceDependency = Annotated[OrchestratorService, Depends(get_orchestrator)]
PatientsServiceDependency = Annotated[PatientsService, Depends(get_patients_service)]
