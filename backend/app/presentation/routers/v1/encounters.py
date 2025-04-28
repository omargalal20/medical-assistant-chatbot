from fastapi import APIRouter
from fhirpy.base.resource_protocol import TResource

from presentation.dependencies import EncountersServiceDependency

router = APIRouter(prefix="/encounters")


@router.get("/recent/patients/{patient_id}")
async def get_recent_encounters(patient_id: str, service: EncountersServiceDependency, count: int = 3):
    encounters = await service.get_recent_encounters(patient_id, count)
    return encounters
