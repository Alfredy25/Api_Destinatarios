from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserRequest(BaseModel):
    username: str = Field(..., min_length=4, max_length=16)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=20, description="contraseña del usuario")

class UserDto(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)