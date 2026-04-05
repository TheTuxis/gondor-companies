from datetime import datetime

from pydantic import BaseModel


class BusinessUnitCreate(BaseModel):
    name: str
    code: str | None = None
    parent_id: int | None = None


class BusinessUnitUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    parent_id: int | None = None


class BusinessUnitResponse(BaseModel):
    id: int
    company_id: int
    name: str
    code: str | None = None
    parent_id: int | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
