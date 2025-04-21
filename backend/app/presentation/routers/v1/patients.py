from fastapi import APIRouter
from fhirclient.models.patient import Patient

from presentation.dependencies import PatientsServiceDependency

router = APIRouter(prefix="/patients")


@router.get("")
def get_many(service: PatientsServiceDependency):
    patients: list[Patient] = service.get_many()
    return [patient.as_json() for patient in patients]


@router.get("/{patient_id}")
def get_one(patient_id: str, service: PatientsServiceDependency):
    patient: Patient = service.get_one(patient_id)
    return patient.as_json() if patient else {"error": "Patient not found"}
