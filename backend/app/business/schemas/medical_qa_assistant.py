from datetime import datetime

from pydantic import BaseModel, Field

from data.models.enums.role import Role


class AssistantResponse(BaseModel):
    id: datetime = Field(...)
    role: Role = Field(...)
    content: str = Field(...)
    created_at: datetime = Field(...)
