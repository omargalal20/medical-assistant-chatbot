from datetime import datetime

from pydantic import BaseModel, Field

from data.models.enums.role import Role


class DoctorQuery(BaseModel):
    id: str = Field(...)
    role: Role = Field(...)
    content: str = Field(...)
    created_at: datetime = Field(...)


class AssistantResponse(BaseModel):
    id: str = Field(...)
    role: Role = Field(...)
    content: str = Field(...)
    created_at: datetime = Field(...)
