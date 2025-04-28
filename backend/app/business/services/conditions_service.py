from typing import Optional

from fastapi import HTTPException, status
from fhirclient.models.condition import Condition
from fhirclient.models.fhirabstractbase import FHIRValidationError
from loguru import logger

from business.dependencies import FHIRServerDependency


class ConditionsService:
    """Service to manage FHIR Condition resources."""

    def __init__(self, fhir_server: FHIRServerDependency):
        """
        Initialize ConditionsService with a FHIR client.
        """
        self.fhir_server = fhir_server

    def get_latest_conditions(self, patient_id: str, count: int = 1) -> Optional[Condition]:
        """
        Retrieve the latest condition for a patient.
        """
        try:
            search = Condition.where(struct={
                "patient": patient_id,
                "_sort": "-onset-date,-abatement-date,-recorded-date",
                "_count": str(count)
            })
            conditions = search.perform_resources(self.fhir_server)
            # There is an issue with the count
            logger.debug(f"Number of conditions: {len(conditions)}")
            return conditions[0] if conditions else None
        except FHIRValidationError as e:
            logger.error(f"FHIRValidationError: {str(e)}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"FHIRValidationError: {str(e)}")
        except Exception as e:
            logger.error(f"Error fetching latest condition for patient {patient_id}: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error fetching latest condition for patient {patient_id}: {str(e)}")
