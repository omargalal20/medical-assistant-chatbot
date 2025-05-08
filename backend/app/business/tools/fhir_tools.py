from typing import Dict, Any, Optional

from fhirpy import AsyncFHIRClient
from fhirpy.lib import AsyncFHIRSearchSet
from langchain_core.tools import StructuredTool
from loguru import logger

from config.settings import get_settings

settings = get_settings()


class FHIRTools:
    """Service to manage FHIR Tools."""

    def __init__(self, fhir_server: AsyncFHIRClient):
        """
        Initialize FHIRTools with a FHIR client.
        """
        self.fhir_server: AsyncFHIRClient = fhir_server
        self.tool = StructuredTool.from_function(
            coroutine=self.get_fhir_resources,
            name="get_fhir_resources",
            parse_docstring=True
        )

    async def get_fhir_resources(self,
                                 resource_type: str,
                                 search_params: Optional[Dict[str, Any]] = None,
                                 limit: Optional[int] = None,
                                 sort: Optional[str] = None,
                                 require_count: Optional[bool] = False) -> Any:
        """
        Retrieves resources from the FHIR server based on the specified resource type and search parameters.

        Args:
            resource_type (str): The type of FHIR resource to retrieve (e.g., 'Patient', 'Observation').
            search_params (Optional[Dict[str, Any]]): A dictionary of search parameters to filter the resources.
                                                      Keys and values should follow FHIR's search parameter syntax.
            limit (Optional[int]): Maximum number of results to retrieve.
            sort (Optional[str]): Sort criteria for the results. Use FHIR-compliant syntax (e.g., '_lastUpdated, -onset-date,-abatement-date,-recorded-date').
            require_count (Optional[bool]): If True, returns the count of matching resources instead of the resources themselves.

        Returns:
            Any: Either the count of resources or a list of resources matching the search criteria.
        """

        logger.info(f"get_fhir_resources called with resource_type={resource_type}, "
                    f"search_params={search_params}, limit={limit}, sort={sort}, require_count={require_count}")

        # Initialize resource search set
        resource: AsyncFHIRSearchSet = self.fhir_server.resources(resource_type).search(**search_params)

        # Apply limit if specified
        if limit:
            resource.limit(limit)

        # Apply sort criteria if specified
        if sort:
            resource.sort(sort)

        # Return the count if requested
        if require_count:
            count = await resource.count()
            logger.info(f"Returning count of resources: {count}")
            return count

        # Fetch and return the resources as a list of dictionaries
        fetched_resources = await resource.fetch()
        logger.info(f"Returning fetched resources: {len(fetched_resources)} resources")
        return fetched_resources
