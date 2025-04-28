from fastapi import APIRouter

from presentation.dependencies import PatientsServiceDependency

router = APIRouter(prefix="/patients")


@router.get("")
async def get_many(service: PatientsServiceDependency):
    patients = await service.get_many()
    return patients


@router.get("/{patient_id}")
async def get_one(patient_id: str, service: PatientsServiceDependency):
    patient = await service.get_one(patient_id)
    return patient
