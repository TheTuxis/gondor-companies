from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business_unit import BusinessUnit
from app.schemas.business_unit import BusinessUnitCreate, BusinessUnitUpdate


class BusinessUnitRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self, company_id: int, page: int = 1, page_size: int = 20) -> tuple[list[BusinessUnit], int]:
        offset = (page - 1) * page_size
        query = (
            select(BusinessUnit)
            .where(BusinessUnit.company_id == company_id, BusinessUnit.is_active.is_(True))
            .offset(offset)
            .limit(page_size)
        )
        result = await self.db.execute(query)
        items = list(result.scalars().all())

        count_query = (
            select(func.count())
            .select_from(BusinessUnit)
            .where(BusinessUnit.company_id == company_id, BusinessUnit.is_active.is_(True))
        )
        total = (await self.db.execute(count_query)).scalar_one()
        return items, total

    async def get_by_id(self, company_id: int, bu_id: int) -> BusinessUnit | None:
        query = select(BusinessUnit).where(BusinessUnit.id == bu_id, BusinessUnit.company_id == company_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, company_id: int, data: BusinessUnitCreate) -> BusinessUnit:
        bu = BusinessUnit(company_id=company_id, **data.model_dump())
        self.db.add(bu)
        await self.db.flush()
        await self.db.refresh(bu)
        return bu

    async def update(self, bu: BusinessUnit, data: BusinessUnitUpdate) -> BusinessUnit:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(bu, field, value)
        await self.db.flush()
        await self.db.refresh(bu)
        return bu

    async def delete(self, bu: BusinessUnit) -> None:
        bu.is_active = False
        await self.db.flush()
