from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.reference.brands.repository import BrandRepository
from app.modules.reference.brands.service import BrandService


def get_brand_repository(
    db: Session = Depends(get_db),
) -> BrandRepository:
    return BrandRepository(db)


def get_brand_service(
    repository: BrandRepository = Depends(get_brand_repository),
) -> BrandService:
    return BrandService(repository)