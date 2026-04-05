from datetime import datetime

from pydantic import BaseModel


class BranchCreate(BaseModel):
    name: str
    address: str | None = None
    city: str | None = None
    country: str | None = None
    phone: str | None = None
    is_headquarters: bool = False


class BranchUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    phone: str | None = None
    is_headquarters: bool | None = None


class BranchResponse(BaseModel):
    id: int
    company_id: int
    name: str
    address: str | None = None
    city: str | None = None
    country: str | None = None
    phone: str | None = None
    is_headquarters: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
