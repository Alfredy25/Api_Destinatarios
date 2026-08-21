from abc import ABC, abstractmethod
from typing import List, Optional

from app.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def find_all(self) -> List[User]:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass