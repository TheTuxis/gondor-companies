from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.branch import Branch
from app.repositories.branch import BranchRepository
from app.schemas.branch import BranchCreate, BranchUpdate


class BranchService:
    def __init__(self, db: AsyncSession):
        self.repo = BranchRepository(db)

    async def get_list(self, company_id: int, page: int = 1, page_size: int = 20) -> tuple[list[Branch], int]:
        return await self.repo.get_list(company_id, page, page_size)

    async def get_by_id(self, company_id: int, branch_id: int) -> Branch:
        branch = await self.repo.get_by_id(company_id, branch_id)
        if not branch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
        return branch

    async def create(self, company_id: int, data: BranchCreate) -> Branch:
        return await self.repo.create(company_id, data)

    async def update(self, company_id: int, branch_id: int, data: BranchUpdate) -> Branch:
        branch = await self.get_by_id(company_id, branch_id)
        return await self.repo.update(branch, data)

    async def delete(self, company_id: int, branch_id: int) -> None:
        branch = await self.get_by_id(company_id, branch_id)
        await self.repo.delete(branch)
