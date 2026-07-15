from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.modules.reference.brands.dependencies import get_brand_service
from app.modules.reference.brands.exceptions import (
    BrandCodeAlreadyExistsError,
    BrandNameAlreadyExistsError,
    BrandNotFoundError,
)
from app.modules.reference.brands.schemas import (
    BrandCreate,
    BrandResponse,
    BrandUpdate,
)
from app.modules.reference.brands.service import BrandService

router = APIRouter(
    prefix="/reference/brands",
    tags=["Reference - Brands"],
)


@router.get(
    "",
    response_model=list[BrandResponse],
)
def get_brands(
    service: BrandService = Depends(get_brand_service),
):
    return service.get_all()


@router.get(
    "/{brand_id}",
    response_model=BrandResponse,
)
def get_brand(
    brand_id: UUID,
    service: BrandService = Depends(get_brand_service),
):
    try:
        return service.get_by_id(brand_id)
    except BrandNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "",
    response_model=BrandResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_brand(
    data: BrandCreate,
    service: BrandService = Depends(get_brand_service),
):
    try:
        return service.create(data)
    except (
        BrandNameAlreadyExistsError,
        BrandCodeAlreadyExistsError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{brand_id}",
    response_model=BrandResponse,
)
def update_brand(
    brand_id: UUID,
    data: BrandUpdate,
    service: BrandService = Depends(get_brand_service),
):
    try:
        return service.update(
            brand_id,
            data,
        )
    except BrandNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except (
        BrandNameAlreadyExistsError,
        BrandCodeAlreadyExistsError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{brand_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_brand(
    brand_id: UUID,
    service: BrandService = Depends(get_brand_service),
):
    try:
        service.delete(brand_id)
    except BrandNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc