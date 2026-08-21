from pydantic import BaseModel, EmailStr, Field

class UserRequest(BaseModel):
    username: str = Field(..., min_length=4, max_length=16)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=20, description="contraseña del usuario")