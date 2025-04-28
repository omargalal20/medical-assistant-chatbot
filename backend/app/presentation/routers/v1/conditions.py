from fastapi import APIRouter

from presentation.dependencies import ConditionsServiceDependency

router = APIRouter(prefix="/conditions")


@router.get("/latest/patients/{patient_id}")
async def get_latest_condition(patient_id: str, service: ConditionsServiceDependency):
    condition = await service.get_latest_conditions(patient_id)
    return condition
