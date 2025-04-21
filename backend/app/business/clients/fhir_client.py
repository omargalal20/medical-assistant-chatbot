from fhirclient import client
from fhirclient.server import FHIRUnauthorizedException, FHIRNotFoundException, FHIRPermissionDeniedException, \
    FHIRServer
from loguru import logger

from config.settings import get_settings

settings = get_settings()


class FHIRClient:
    """FHIR Client"""

    def __init__(self):
        """Initialize FHIR Client configuration."""
        self.fhir_client = None
        self.fhir_client_settings = {
            'app_id': settings.FHIR_CLIENT_APP_ID,
            'api_base': settings.FHIR_CLIENT_API_BASE
        }

    def initialize(self):
        """Return the configured FHIR server instance."""
        try:
            self.fhir_client = client.FHIRClient(settings=self.fhir_client_settings)

            logger.info(f"Is FHIR Server Prepared: {self.fhir_client.prepare()}")
            logger.info(f"Is FHIR Server Ready: {self.fhir_client.ready}")

        except FHIRNotFoundException as e:
            logger.error(f"FHIRNotFoundException: {str(e)}")
            raise RuntimeError(f"FHIRNotFoundException: {str(e)}")
        except FHIRUnauthorizedException as e:
            logger.error(f"FHIRUnauthorizedException: {str(e)}")
            raise RuntimeError(f"FHIRUnauthorizedException: {str(e)}")
        except FHIRPermissionDeniedException as e:
            logger.error(f"FHIRPermissionDeniedException: {str(e)}")
            raise RuntimeError(f"FHIRPermissionDeniedException: {str(e)}")
        except Exception as e:
            logger.error(f"FHIR Client failed to instantiate: {str(e)}")
            raise RuntimeError("FHIR Client failed to instantiate.") from e

    def get_fhir_server(self) -> FHIRServer:
        """Return the configured FHIR server instance."""
        return self.fhir_client.server


fhir_client_interface = FHIRClient()
