from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.di import get_user_repository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, TokenDto
from app.security.jwt import create_access_token
from app.security.passwords import verify_password

router = APIRouter(prefix="/auth", tags=["oauth"])

# Endpoint de login
@router.post("/login", response_model=TokenDto)
def login(data: LoginRequest, repository: UserRepository = Depends(get_user_repository)):
    user = repository.find_by_email(str(data.email))

    if not user or not user.is_active or not verify_password(data.password, str(user.password_hash)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
    token = create_access_token(subject=str(user.id))
    return TokenDto(access_token=token)

@router.post("/token/form", response_model=TokenDto)
def login_form(data_form: OAuth2PasswordRequestForm = Depends(),
               repository: UserRepository = Depends(get_user_repository)):

    return login(LoginRequest.model_validate({
        "email": data_form.username,
        "password": data_form.password
    }), repository)