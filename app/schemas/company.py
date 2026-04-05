from datetime import datetime

from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    legal_name: str | None = None
    tax_id: str | None = None
    industry: str | None = None
    website: str | None = None
    logo_url: str | None = None


class CompanyUpdate(BaseModel):
    name: str | None = None
    legal_name: str | None = None
    tax_id: str | None = None
    industry: str | None = None
    website: str | None = None
    logo_url: str | None = None


class CompanyResponse(BaseModel):
    id: int
    name: str
    legal_name: str | None = None
    tax_id: str | None = None
    industry: str | None = None
    website: str | None = None
    logo_url: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
