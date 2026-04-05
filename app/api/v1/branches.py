from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import CurrentUser, get_current_user
from app.schemas.branch import BranchCreate, BranchResponse, BranchUpdate
from app.schemas.common import PaginatedResponse
from app.services.branch import BranchService

router = APIRouter()


@router.get("/companies/{company_id}/branches", response_model=PaginatedResponse[BranchResponse])
async def list_branches(
    company_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = BranchService(db)
    items, total = await service.get_list(company_id, page, page_size)
    return PaginatedResponse(
        items=[BranchResponse.model_validate(b) for b in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/companies/{company_id}/branches", response_model=BranchResponse, status_code=201)
async def create_branch(
    company_id: int,
    data: BranchCreate,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = BranchService(db)
    branch = await service.create(company_id, data)
    return BranchResponse.model_validate(branch)


@router.get("/companies/{company_id}/branches/{branch_id}", response_model=BranchResponse)
async def get_branch(
    company_id: int,
    branch_id: int,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = BranchService(db)
    branch = await service.get_by_id(company_id, branch_id)
    return BranchResponse.model_validate(branch)


@router.put("/companies/{company_id}/branches/{branch_id}", response_model=BranchResponse)
async def update_branch(
    company_id: int,
    branch_id: int,
    data: BranchUpdate,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = BranchService(db)
    branch = await service.update(company_id, branch_id, data)
    return BranchResponse.model_validate(branch)


@router.delete("/companies/{company_id}/branches/{branch_id}", status_code=204)
async def delete_branch(
    company_id: int,
    branch_id: int,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = BranchService(db)
    await service.delete(company_id, branch_id)
