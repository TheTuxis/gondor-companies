from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business_unit import BusinessUnit
from app.repositories.business_unit import BusinessUnitRepository
from app.schemas.business_unit import BusinessUnitCreate, BusinessUnitUpdate


class BusinessUnitService:
    def __init__(self, db: AsyncSession):
        self.repo = BusinessUnitRepository(db)

    async def get_list(self, company_id: int, page: int = 1, page_size: int = 20) -> tuple[list[BusinessUnit], int]:
        return await self.repo.get_list(company_id, page, page_size)

    async def get_by_id(self, company_id: int, bu_id: int) -> BusinessUnit:
        bu = await self.repo.get_by_id(company_id, bu_id)
        if not bu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business unit not found")
        return bu

    async def create(self, company_id: int, data: BusinessUnitCreate) -> BusinessUnit:
        return await self.repo.create(company_id, data)

    async def update(self, company_id: int, bu_id: int, data: BusinessUnitUpdate) -> BusinessUnit:
        bu = await self.get_by_id(company_id, bu_id)
        return await self.repo.update(bu, data)

    async def delete(self, company_id: int, bu_id: int) -> None:
        bu = await self.get_by_id(company_id, bu_id)
        await self.repo.delete(bu)
