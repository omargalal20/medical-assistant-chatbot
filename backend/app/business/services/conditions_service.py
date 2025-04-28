from fastapi import HTTPException, status
from fhirpy import AsyncFHIRClient
from fhirpy.base.exceptions import BaseFHIRError, MultipleResourcesFound
from fhirpy.lib import AsyncFHIRSearchSet
from loguru import logger

from business.dependencies import FHIRServerDependency


class ConditionsService:
    """Service to manage FHIR Condition resources."""

    def __init__(self, fhir_server: FHIRServerDependency):
        """
        Initialize ConditionsService with a FHIR client.
        """
        self.fhir_server: AsyncFHIRClient = fhir_server
        self.conditions: AsyncFHIRSearchSet = self.fhir_server.resources('Condition')

    async def get_latest_conditions(self, patient_id: str, count: int = 1):
        """
        Retrieve the latest conditions for a patient.
        """
        try:
            latest_conditions = (
                await self.conditions.search(patient=patient_id).limit(count).sort(
                    "-onset-date,-abatement-date,-recorded-date").fetch()
            )
            logger.debug(f"Number of conditions: {len(latest_conditions)}")
            return latest_conditions
        except MultipleResourcesFound as e:
            logger.error(f"MultipleResourcesFound: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"MultipleResourcesFound: {str(e)}"
            )
        except BaseFHIRError as e:
            logger.error(f"BaseFHIRError: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"BaseFHIRError: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error fetching latest conditions for patient {patient_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching latest conditions for patient {patient_id}: {str(e)}"
            )
