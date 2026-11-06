from pydantic import BaseModel, Field, EmailStr


# Schema: LoginRequest
# Datos que el cliente envía para autenticarse
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field( ..., min_length=4, max_length=20, examples=["password_seguro"])


# Schema: TokenResponse
# -----------------------------------------------------------------------------
# Respuesta estándar de autenticación con JWT
class TokenDto(BaseModel):
    access_token: str
    token_type: str = 'bearer'

