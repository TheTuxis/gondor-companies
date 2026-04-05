from datetime import datetime

from pydantic import BaseModel


class SettingUpsert(BaseModel):
    value: str


class SettingResponse(BaseModel):
    id: int
    company_id: int
    key: str
    value: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
