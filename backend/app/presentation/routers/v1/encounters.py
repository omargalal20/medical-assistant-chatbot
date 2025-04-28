from fastapi import APIRouter
from fhirclient.models.encounter import Encounter

from presentation.dependencies import EncountersServiceDependency

router = APIRouter(prefix="/encounters")


@router.get("/recent/patients/{patient_id}")
def get_recent_encounters(patient_id: str, service: EncountersServiceDependency, count: int = 3):
    encounters: list[Encounter] = service.get_recent_encounters(patient_id, count)
    return [encounter.as_json() for encounter in encounters]
