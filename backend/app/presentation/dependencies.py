from typing import Annotated

from fastapi import Depends

from business.dependencies import LLMClientDependency, RetrieverClientDependency, FHIRServerDependency, \
    TranslatorAgentDependency
from business.services.conditions_service import ConditionsService
from business.services.encounters_service import EncountersService
from business.services.orchestrator_service import OrchestratorService
from business.services.patients_service import PatientsService


def get_orchestrator(llm_client: LLMClientDependency,
                     retriever_client: RetrieverClientDependency,
                     fhir_translator_agent: TranslatorAgentDependency) -> OrchestratorService:
    """Provide a configured orchestrator."""
    return OrchestratorService(llm_client, retriever_client, fhir_translator_agent)


def get_patients_service(
        fhir_server: FHIRServerDependency
) -> PatientsService:
    return PatientsService(fhir_server)


def get_encounters_service(
        fhir_server: FHIRServerDependency
) -> EncountersService:
    return EncountersService(fhir_server)


def get_conditions_service(
        fhir_server: FHIRServerDependency
) -> ConditionsService:
    return ConditionsService(fhir_server)


OrchestratorServiceDependency = Annotated[OrchestratorService, Depends(get_orchestrator)]
PatientsServiceDependency = Annotated[PatientsService, Depends(get_patients_service)]
EncountersServiceDependency = Annotated[EncountersService, Depends(get_encounters_service)]
ConditionsServiceDependency = Annotated[ConditionsService, Depends(get_conditions_service)]
