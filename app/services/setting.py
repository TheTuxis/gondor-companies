from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.setting import CompanySetting
from app.repositories.setting import SettingRepository


class SettingService:
    def __init__(self, db: AsyncSession):
        self.repo = SettingRepository(db)

    async def get_all(self, company_id: int) -> list[CompanySetting]:
        return await self.repo.get_all(company_id)

    async def get_by_key(self, company_id: int, key: str) -> CompanySetting:
        setting = await self.repo.get_by_key(company_id, key)
        if not setting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Setting '{key}' not found")
        return setting

    async def upsert(self, company_id: int, key: str, value: str) -> CompanySetting:
        return await self.repo.upsert(company_id, key, value)

    async def delete(self, company_id: int, key: str) -> None:
        setting = await self.get_by_key(company_id, key)
        await self.repo.delete(setting)
