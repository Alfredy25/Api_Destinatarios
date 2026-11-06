from abc import ABC, abstractmethod
from typing import List
from app.api.v1.user.schemas import UserDto, UserRequest
from app.api.v1.user.repository import UserRepository
from sqlalchemy.orm import Session
from app.entities.user import User
from app.core.security import hash_password

class UserService(ABC):

    @abstractmethod
    def find_all(self) -> List[UserDto]:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> UserDto | None:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> UserDto | None:
        pass

    @abstractmethod
    def create(self, user: UserRequest) -> UserRequest:
        pass


class UserServiceImpl(UserService):

    def __init__(self, repo: UserRepository, db: Session):
        self._repo = repo
        self._db = db

    def find_all(self) -> List[UserDto]:
        return [UserDto.model_validate(user) for user in self._repo.find_all()]

    def find_by_id(self, user_id: int) -> UserDto | None:
        user = self._repo.find_by_id(user_id)
        if not user:
            return None
        return UserDto.model_validate(user)

    def find_by_email(self, email: str) -> UserDto | None:
        user = self._repo.find_by_email(email)
        if not user:
            return None
        return UserDto.model_validate(user)

    def create(self, user: UserRequest) -> UserDto:
        if self._repo.find_by_email(str(user.email)):
            raise ValueError('Email ya existe')
        user_entity = User(username=user.username ,email=user.email, password_hash=hash_password(user.password))
        try:
            self._repo.create(user_entity)
            self._db.commit()
            self._db.refresh(user_entity)
            return UserDto.model_validate(user_entity)
        except Exception:
            self._db.rollback()
            raise