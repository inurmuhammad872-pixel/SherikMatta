from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.modules.identity.repositories.user_repository import UserRepository
from app.modules.identity.schemas.user_create import UserCreate
from app.modules.identity.schemas.user_response import UserResponse
from app.modules.identity.services.auth_service import AuthService
from app.modules.identity.schemas.user_login import UserLogin
from app.modules.identity.schemas.token import Token

from app.core.security.dependencies import get_current_user
from app.modules.identity.models.user import User
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    repository = UserRepository(db)
    service = AuthService(repository)

    try:
        return service.register(user_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    
@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    repository = UserRepository(db)
    service = AuthService(repository)

    try:
        return service.login(
            form_data.username,
            form_data.password,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc),
        ) from exc
    
@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
):
    return current_user