from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=100,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )