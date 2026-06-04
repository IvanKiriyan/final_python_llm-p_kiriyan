from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import UserAlreadyExistsError, InvalidCredentialsError, UserNotFoundError
from app.repositories.users import UserRepository
from app.schemas.auth import TokenResponse
from app.schemas.user import UserPublic


class Authentication:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, email: str, password: str) -> UserPublic: # регситрация
        existing = await self.repo.get_by_email(email)
        if existing:
            raise UserAlreadyExistsError()
        hashed = hash_password(password)
        user = await self.repo.create(email=email, password_hash=hashed)
        return UserPublic.model_validate(user)
    
    async def login(self, email: str, password: str) -> TokenResponse: # логин
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        token = create_access_token(sub=str(user.id), role=user.role)
        return TokenResponse(access_token=token)
    
    async def me(self, user_id: int) -> UserPublic: # проверка существования пользователя
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return UserPublic.model_validate(user)