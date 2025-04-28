from fastapi import APIRouter
from fhirclient.models.condition import Condition

from presentation.dependencies import ConditionsServiceDependency

router = APIRouter(prefix="/conditions")


@router.get("/latest/patients/{patient_id}")
def get_latest_condition(patient_id: str, service: ConditionsServiceDependency):
    condition: Condition = service.get_latest_conditions(patient_id)
    return condition.as_json() if condition else {"Condition": "No conditions found for this patient"}
