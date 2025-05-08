from fastapi import HTTPException, status
from fhirpy import AsyncFHIRClient
from fhirpy.base.exceptions import BaseFHIRError, MultipleResourcesFound
from fhirpy.lib import AsyncFHIRSearchSet
from loguru import logger


class EncountersService:
    """Service to manage FHIR Encounter resources."""

    def __init__(self, fhir_server: AsyncFHIRClient):
        """
        Initialize EncountersService with a FHIR client.
        """
        self.fhir_server: AsyncFHIRClient = fhir_server
        self.encounters: AsyncFHIRSearchSet = self.fhir_server.resources('Encounter')

    async def get_recent_encounters(self, patient_id: str, count: int = 3):
        """
        Retrieve recent encounters for a patient.
        """
        try:
            recent_encounters = await self.encounters.search(patient=patient_id).limit(count).sort(
                "-_lastUpdated").fetch()
            logger.debug(f"Number of encounters: {len(recent_encounters)}")
            return recent_encounters
        except MultipleResourcesFound as e:
            logger.error(f"MultipleResourcesFound: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"MultipleResourcesFound: {str(e)}")
        except BaseFHIRError as e:
            logger.error(f"BaseFHIRError:{str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error retrieving patients: {str(e)}")
