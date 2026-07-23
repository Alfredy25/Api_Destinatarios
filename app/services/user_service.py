from abc import ABC, abstractmethod
from typing import List

from app.schemas.user_dto import UserDto
from app.schemas.user_request import UserRequest


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
