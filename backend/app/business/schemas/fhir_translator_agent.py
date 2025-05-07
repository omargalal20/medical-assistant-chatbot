from typing import Optional

from pydantic import BaseModel, Field


class FHIRTranslatorAgentOutput(BaseModel):
    intent: str = Field(..., description="The primary goal of the query.")
    entities: dict = Field(..., description="Key entities extracted from the query.")
    ambiguities: Optional[list] = Field(None, description="Any ambiguities or missing details.")
    fhir_query: str = Field(..., description="The translated FHIR API query string.")
