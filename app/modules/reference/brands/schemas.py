from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BrandCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    code: str = Field(
        min_length=2,
        max_length=20,
    )

    country: str = Field(
        min_length=2,
        max_length=100,
    )

    logo: str | None = None

    is_active: bool = True


class BrandUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    code: str | None = Field(
        default=None,
        min_length=2,
        max_length=20,
    )

    country: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    logo: str | None = None

    is_active: bool | None = None


class BrandResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    name: str
    code: str
    country: str
    logo: str | None
    is_active: bool

    created_at: datetime
    updated_at: datetime


class BrandListResponse(BaseModel):
    items: list[BrandResponse]
    total: int