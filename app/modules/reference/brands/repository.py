from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.reference.brands.models import Brand


class BrandRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Brand]:
        stmt = select(Brand).order_by(Brand.name)
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, brand_id: UUID) -> Brand | None:
        stmt = select(Brand).where(Brand.id == brand_id)
        return self.db.scalar(stmt)

    def get_by_name(self, name: str) -> Brand | None:
        stmt = select(Brand).where(Brand.name == name)
        return self.db.scalar(stmt)

    def get_by_code(self, code: str) -> Brand | None:
        stmt = select(Brand).where(Brand.code == code)
        return self.db.scalar(stmt)

    def create(self, brand: Brand) -> Brand:
        self.db.add(brand)
        self.db.commit()
        self.db.refresh(brand)
        return brand

    def update(self, brand: Brand) -> Brand:
        self.db.commit()
        self.db.refresh(brand)
        return brand

    def delete(self, brand: Brand) -> None:
        self.db.delete(brand)
        self.db.commit()