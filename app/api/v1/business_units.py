from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import CurrentUser, get_current_user
from app.schemas.business_unit import BusinessUnitCreate, BusinessUnitResponse, BusinessUnitUpdate
from app.schemas.common import PaginatedResponse
from app.services.business_unit import BusinessUnitService

router = APIRouter()


@router.get("/companies/{company_id}/business-units", response_model=PaginatedResponse[BusinessUnitResponse])
async def list_business_units(
    company_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = BusinessUnitService(db)
    items, total = await service.get_list(company_id, page, page_size)
    return PaginatedResponse(
        items=[BusinessUnitResponse.model_validate(bu) for bu in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/companies/{company_id}/business-units", response_model=BusinessUnitResponse, status_code=201)
async def create_business_unit(
    company_id: int,
    data: BusinessUnitCreate,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = BusinessUnitService(db)
    bu = await service.create(company_id, data)
    return BusinessUnitResponse.model_validate(bu)


@router.get("/companies/{company_id}/business-units/{bu_id}", response_model=BusinessUnitResponse)
async def get_business_unit(
    company_id: int,
    bu_id: int,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = BusinessUnitService(db)
    bu = await service.get_by_id(company_id, bu_id)
    return BusinessUnitResponse.model_validate(bu)


@router.put("/companies/{company_id}/business-units/{bu_id}", response_model=BusinessUnitResponse)
async def update_business_unit(
    company_id: int,
    bu_id: int,
    data: BusinessUnitUpdate,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = BusinessUnitService(db)
    bu = await service.update(company_id, bu_id, data)
    return BusinessUnitResponse.model_validate(bu)


@router.delete("/companies/{company_id}/business-units/{bu_id}", status_code=204)
async def delete_business_unit(
    company_id: int,
    bu_id: int,
    db: AsyncSession = Depends(get_db),
    _user: CurrentUser = Depends(get_current_user),
):
    service = BusinessUnitService(db)
    await service.delete(company_id, bu_id)
