from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.dependencies.di import get_user_service
from app.dependencies.security import get_current_user
from app.schemas.user_dto import UserDto
from app.schemas.user_request import UserRequest
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserDto])
def list_users(service: UserService = Depends(get_user_service),
               current_user = Depends(get_current_user)):
    return service.find_all()

@router.get('/{user_id}', response_model=UserDto)
def get_user(user_id: int, service: UserService = Depends(get_user_service),
             current_user = Depends(get_current_user)):

    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No se pueden ver usuarios de otros")

    user = service.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no existe")

    return user

@router.post("/", response_model=UserDto, status_code=status.HTTP_201_CREATED)
def create_user(user: UserRequest = Body(...), service: UserService = Depends(get_user_service),
                current_user = Depends(get_current_user)):

    try:
        return service.create(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))