from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.setting import CompanySetting


class SettingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, company_id: int) -> list[CompanySetting]:
        query = select(CompanySetting).where(CompanySetting.company_id == company_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_key(self, company_id: int, key: str) -> CompanySetting | None:
        query = select(CompanySetting).where(CompanySetting.company_id == company_id, CompanySetting.key == key)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def upsert(self, company_id: int, key: str, value: str) -> CompanySetting:
        existing = await self.get_by_key(company_id, key)
        if existing:
            existing.value = value
            await self.db.flush()
            await self.db.refresh(existing)
            return existing
        setting = CompanySetting(company_id=company_id, key=key, value=value)
        self.db.add(setting)
        await self.db.flush()
        await self.db.refresh(setting)
        return setting

    async def delete(self, setting: CompanySetting) -> None:
        await self.db.delete(setting)
        await self.db.flush()
