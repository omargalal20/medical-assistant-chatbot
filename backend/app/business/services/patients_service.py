from fastapi import HTTPException, status
from fhirpy import AsyncFHIRClient
from fhirpy.base.exceptions import BaseFHIRError, ResourceNotFound, MultipleResourcesFound
from fhirpy.lib import AsyncFHIRSearchSet
from loguru import logger

from business.dependencies import FHIRServerDependency


class PatientsService:
    """Service to manage FHIR Patient resources."""

    def __init__(self, fhir_server: FHIRServerDependency):
        """
        Initialize PatientsService with a FHIR client.
        """
        self.fhir_server: AsyncFHIRClient = fhir_server
        self.patients: AsyncFHIRSearchSet = self.fhir_server.resources('Patient')

    async def get_one(self, patient_id: str):
        """
        Retrieve a single Patient resource by ID.
        """
        try:
            patient = await self.patients.get(patient_id)
            return patient
        except ResourceNotFound as e:
            logger.error(f"ResourceNotFound: {str(e)}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient {patient_id} Not Found")
        except BaseFHIRError as e:
            logger.error(f"BaseFHIRError: {patient_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error retrieving patient {patient_id}: {str(e)}")

    async def get_many(self):
        """
        Retrieve all patients.
        """
        try:
            patients = await self.patients.fetch()  # No filters applied
            return patients
        except MultipleResourcesFound as e:
            logger.error(f"MultipleResourcesFound: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"MultipleResourcesFound: {str(e)}")
        except BaseFHIRError as e:
            logger.error(f"BaseFHIRError:{str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error retrieving patients: {str(e)}")
