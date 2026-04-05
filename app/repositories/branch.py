from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.branch import Branch
from app.schemas.branch import BranchCreate, BranchUpdate


class BranchRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self, company_id: int, page: int = 1, page_size: int = 20) -> tuple[list[Branch], int]:
        offset = (page - 1) * page_size
        query = (
            select(Branch)
            .where(Branch.company_id == company_id, Branch.is_active.is_(True))
            .offset(offset)
            .limit(page_size)
        )
        result = await self.db.execute(query)
        items = list(result.scalars().all())

        count_query = (
            select(func.count()).select_from(Branch).where(Branch.company_id == company_id, Branch.is_active.is_(True))
        )
        total = (await self.db.execute(count_query)).scalar_one()
        return items, total

    async def get_by_id(self, company_id: int, branch_id: int) -> Branch | None:
        query = select(Branch).where(Branch.id == branch_id, Branch.company_id == company_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, company_id: int, data: BranchCreate) -> Branch:
        branch = Branch(company_id=company_id, **data.model_dump())
        self.db.add(branch)
        await self.db.flush()
        await self.db.refresh(branch)
        return branch

    async def update(self, branch: Branch, data: BranchUpdate) -> Branch:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(branch, field, value)
        await self.db.flush()
        await self.db.refresh(branch)
        return branch

    async def delete(self, branch: Branch) -> None:
        branch.is_active = False
        await self.db.flush()
