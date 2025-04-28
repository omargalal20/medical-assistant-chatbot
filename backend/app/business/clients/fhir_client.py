from fhirpy import AsyncFHIRClient
from fhirpy.base.exceptions import AuthorizationError, BaseFHIRError
from loguru import logger

from config.settings import get_settings

settings = get_settings()


class FHIRClient:
    """FHIR Client"""

    def __init__(self):
        """Initialize FHIR Client configuration."""
        self.fhir_client = None

    def initialize(self):
        """Return the configured FHIR server instance."""
        try:
            self.fhir_client: AsyncFHIRClient = AsyncFHIRClient(
                settings.FHIR_CLIENT_API_BASE,
            )

            logger.info("FHIR Client Initialized")

        except AuthorizationError as e:
            logger.error(f"FHIRUnauthorizedException: {str(e)}")
            raise RuntimeError(f"FHIRUnauthorizedException: {str(e)}")
        except BaseFHIRError as e:
            logger.error(f"FHIR Client failed to instantiate: {str(e)}")
            raise RuntimeError("FHIR Client failed to instantiate.") from e

    def get_fhir_server(self) -> AsyncFHIRClient:
        """Return the configured FHIR server instance."""
        return self.fhir_client


fhir_client = FHIRClient()
