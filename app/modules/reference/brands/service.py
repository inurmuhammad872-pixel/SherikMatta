from uuid import UUID

from app.modules.reference.brands.constants import (
    BRAND_CODE_ALREADY_EXISTS,
    BRAND_NAME_ALREADY_EXISTS,
    BRAND_NOT_FOUND,
)
from app.modules.reference.brands.exceptions import (
    BrandCodeAlreadyExistsError,
    BrandNameAlreadyExistsError,
    BrandNotFoundError,
)
from app.modules.reference.brands.models import Brand
from app.modules.reference.brands.repository import BrandRepository
from app.modules.reference.brands.schemas import (
    BrandCreate,
    BrandUpdate,
)


class BrandService:
    def __init__(self, repository: BrandRepository):
        self.repository = repository

    def get_all(self) -> list[Brand]:
        return self.repository.get_all()

    def get_by_id(self, brand_id: UUID) -> Brand:
        brand = self.repository.get_by_id(brand_id)

        if brand is None:
            raise BrandNotFoundError(BRAND_NOT_FOUND)

        return brand

    def create(self, data: BrandCreate) -> Brand:
        if self.repository.get_by_name(data.name):
            raise BrandNameAlreadyExistsError(
                BRAND_NAME_ALREADY_EXISTS
            )

        if self.repository.get_by_code(data.code):
            raise BrandCodeAlreadyExistsError(
                BRAND_CODE_ALREADY_EXISTS
            )

        brand = Brand(
            name=data.name,
            code=data.code,
            country=data.country,
            logo=data.logo,
            is_active=data.is_active,
        )

        return self.repository.create(brand)

    def update(
        self,
        brand_id: UUID,
        data: BrandUpdate,
    ) -> Brand:
        brand = self.get_by_id(brand_id)

        if (
            data.name is not None
            and data.name != brand.name
            and self.repository.get_by_name(data.name)
        ):
            raise BrandNameAlreadyExistsError(
                BRAND_NAME_ALREADY_EXISTS
            )

        if (
            data.code is not None
            and data.code != brand.code
            and self.repository.get_by_code(data.code)
        ):
            raise BrandCodeAlreadyExistsError(
                BRAND_CODE_ALREADY_EXISTS
            )

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(brand, field, value)

        return self.repository.update(brand)

    def delete(self, brand_id: UUID) -> None:
        brand = self.get_by_id(brand_id)

        self.repository.delete(brand)