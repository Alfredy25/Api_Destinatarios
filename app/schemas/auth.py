from pydantic import BaseModel, Field


# Schema: LoginRequest
# -----------------------------------------------------------------------------
# Datos que el cliente envía para autenticarse
class LoginRequest(BaseModel):
    username: str = Field(..., examples=["operador1"])
    password: str = Field( ..., examples=["password_seguro"])


# Schema: TokenResponse
# -----------------------------------------------------------------------------
# Respuesta estándar de autenticación con JWT
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'

