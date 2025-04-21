from typing import List, Optional

from fastapi import HTTPException, status
from fhirclient.models.fhirabstractbase import FHIRValidationError
from fhirclient.models.patient import Patient
from fhirclient.server import FHIRNotFoundException
from loguru import logger

from business.dependencies import FHIRServerDependency


class PatientsService:
    """Service to manage FHIR Patient resources."""

    def __init__(self, fhir_server: FHIRServerDependency):
        """
        Initialize PatientsService with a FHIR client.
        """
        self.fhir_server = fhir_server

    def get_one(self, patient_id: str) -> Optional[Patient]:
        """
        Retrieve a single Patient resource by ID.
        """
        try:
            patient: Patient = Patient.read(patient_id, self.fhir_server)
            return patient
        except FHIRValidationError as e:
            logger.error(f"FHIRValidationError: {str(e)}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"FHIRValidationError: {str(e)}")
        except FHIRNotFoundException as e:
            logger.error(f"FHIRNotFoundException: {str(e)}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient {patient_id} Not Found")
        except Exception as e:
            logger.error(f"Error retrieving patient {patient_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error retrieving patient {patient_id}: {str(e)}")

    def get_many(self) -> List[Patient]:
        """
        Retrieve all patients.
        """
        try:
            search = Patient.where(struct={})  # No filters applied
            patients = search.perform_resources(self.fhir_server)
            return patients
        except Exception as e:
            logger.error(f"Error fetching patients: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error fetching patients: {str(e)}")
