from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import CurrentUser, get_current_user
from app.schemas.common import PaginatedResponse
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.services.company import CompanyService

router = APIRouter()


@router.get("/companies", response_model=PaginatedResponse[CompanyResponse])
async def list_companies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = CompanyService(db)
    items, total = await service.get_list(page, page_size)
    return PaginatedResponse(
        items=[CompanyResponse.model_validate(c) for c in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/companies", response_model=CompanyResponse, status_code=201)
async def create_company(
    data: CompanyCreate,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = CompanyService(db)
    company = await service.create(data)
    return CompanyResponse.model_validate(company)


@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = CompanyService(db)
    company = await service.get_by_id(company_id)
    return CompanyResponse.model_validate(company)


@router.put("/companies/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    data: CompanyUpdate,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = CompanyService(db)
    company = await service.update(company_id, data)
    return CompanyResponse.model_validate(company)


@router.delete("/companies/{company_id}", response_model=CompanyResponse)
async def delete_company(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = CompanyService(db)
    company = await service.soft_delete(company_id)
    return CompanyResponse.model_validate(company)
