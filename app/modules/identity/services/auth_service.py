from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.modules.identity.models.user import User
from app.modules.identity.repositories.user_repository import UserRepository
from app.modules.identity.schemas.token import Token
from app.modules.identity.schemas.user_create import UserCreate


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, data: UserCreate) -> User:
        existing_user = self.repository.get_by_username(data.username)

        if existing_user:
            raise ValueError("Username already exists.")

        user = User(
            username=data.username,
            password_hash=hash_password(data.password),
        )

        return self.repository.create(user)

    def login(self, username: str, password: str) -> Token:
        user = self.repository.get_by_username(username)

        if user is None:
            raise ValueError("Invalid username or password.")

        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid username or password.")

        token = create_access_token(subject=str(user.id))

        return Token(
            access_token=token,
        )