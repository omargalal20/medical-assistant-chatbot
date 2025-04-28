from typing import List

from fastapi import HTTPException, status
from fhirclient.models.encounter import Encounter
from fhirclient.models.fhirabstractbase import FHIRValidationError
from loguru import logger

from business.dependencies import FHIRServerDependency


class EncountersService:
    """Service to manage FHIR Encounter resources."""

    def __init__(self, fhir_server: FHIRServerDependency):
        """
        Initialize EncountersService with a FHIR client.
        """
        self.fhir_server = fhir_server

    def get_recent_encounters(self, patient_id: str, count: int = 3) -> List[Encounter]:
        """
        Retrieve recent encounters for a patient.
        """
        try:
            search = Encounter.where(struct={
                "patient": patient_id,
                "_sort": "-_lastUpdated",
                "_count": str(count)
            })
            encounters = search.perform_resources(self.fhir_server)
            # There is an issue with the count
            logger.debug(f"Number of encounters: {len(encounters)}")
            return encounters
        except FHIRValidationError as e:
            logger.error(f"FHIRValidationError: {str(e)}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"FHIRValidationError: {str(e)}")
        except Exception as e:
            logger.error(f"Error fetching encounters for patient {patient_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error fetching encounters for patient {patient_id}: {str(e)}")
