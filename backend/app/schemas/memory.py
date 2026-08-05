import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MemoryCreate(BaseModel):
    user_id: str
    role: str
    content: str


class MemoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: str
    role: str
    content: str
    created_at: datetime


class MemoryDeleteResponse(BaseModel):
    status: str
