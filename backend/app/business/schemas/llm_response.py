from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    response: str = Field(...)
