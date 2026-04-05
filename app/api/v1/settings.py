from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import CurrentUser, get_current_user
from app.schemas.setting import SettingResponse, SettingUpsert
from app.services.setting import SettingService

router = APIRouter()


@router.get("/companies/{company_id}/settings", response_model=list[SettingResponse])
async def list_settings(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = SettingService(db)
    items = await service.get_all(company_id)
    return [SettingResponse.model_validate(s) for s in items]


@router.get("/companies/{company_id}/settings/{key}", response_model=SettingResponse)
async def get_setting(
    company_id: int,
    key: str,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = SettingService(db)
    setting = await service.get_by_key(company_id, key)
    return SettingResponse.model_validate(setting)


@router.put("/companies/{company_id}/settings/{key}", response_model=SettingResponse)
async def upsert_setting(
    company_id: int,
    key: str,
    data: SettingUpsert,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = SettingService(db)
    setting = await service.upsert(company_id, key, data.value)
    return SettingResponse.model_validate(setting)


@router.delete("/companies/{company_id}/settings/{key}", status_code=204)
async def delete_setting(
    company_id: int,
    key: str,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = SettingService(db)
    await service.delete(company_id, key)
