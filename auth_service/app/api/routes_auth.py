from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_uc, get_current_user_id
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import Authentication

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserPublic, #эндпоинт регистрации
             status_code=201)
async def register(
    body: RegisterRequest,
    uc: Authentication = Depends(get_auth_uc),
):
    return await uc.register(email=body.email, password=body.password)

@router.post("/login", response_model=TokenResponse) #эндпоинт логина
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    uc: Authentication = Depends(get_auth_uc),
):
    return await uc.login(email=form.username, password=form.password)

@router.get("/me", response_model=UserPublic) #эндпоинт профиля
async def me(
    user_id: int = Depends(get_current_user_id),
    uc: Authentication = Depends(get_auth_uc),
):
    return await uc.me(user_id=user_id)