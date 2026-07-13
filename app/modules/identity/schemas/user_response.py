from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: UUID
    username: str
    is_active: bool
    is_verified: bool

    model_config = ConfigDict(
        from_attributes=True,
    )