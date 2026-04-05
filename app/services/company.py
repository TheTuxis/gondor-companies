from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company
from app.repositories.company import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyService:
    def __init__(self, db: AsyncSession):
        self.repo = CompanyRepository(db)

    async def get_list(self, page: int = 1, page_size: int = 20) -> tuple[list[Company], int]:
        return await self.repo.get_list(page, page_size)

    async def get_by_id(self, company_id: int) -> Company:
        company = await self.repo.get_by_id(company_id)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        return company

    async def create(self, data: CompanyCreate) -> Company:
        return await self.repo.create(data)

    async def update(self, company_id: int, data: CompanyUpdate) -> Company:
        company = await self.get_by_id(company_id)
        return await self.repo.update(company, data)

    async def soft_delete(self, company_id: int) -> Company:
        company = await self.get_by_id(company_id)
        return await self.repo.soft_delete(company)
