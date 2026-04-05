from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self, page: int = 1, page_size: int = 20) -> tuple[list[Company], int]:
        offset = (page - 1) * page_size
        query = select(Company).where(Company.is_active.is_(True)).offset(offset).limit(page_size)
        result = await self.db.execute(query)
        items = list(result.scalars().all())

        count_query = select(func.count()).select_from(Company).where(Company.is_active.is_(True))
        total = (await self.db.execute(count_query)).scalar_one()
        return items, total

    async def get_by_id(self, company_id: int) -> Company | None:
        query = select(Company).where(Company.id == company_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: CompanyCreate) -> Company:
        company = Company(**data.model_dump())
        self.db.add(company)
        await self.db.flush()
        await self.db.refresh(company)
        return company

    async def update(self, company: Company, data: CompanyUpdate) -> Company:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(company, field, value)
        await self.db.flush()
        await self.db.refresh(company)
        return company

    async def soft_delete(self, company: Company) -> Company:
        company.is_active = False
        await self.db.flush()
        await self.db.refresh(company)
        return company
