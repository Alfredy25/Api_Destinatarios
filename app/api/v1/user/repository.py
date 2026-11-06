from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
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



class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, db: Session):
        self._db = db

    def find_all(self) -> List[User]:
        stmt = select(User).order_by(User.id.asc())
        return list(self._db.scalars(stmt).all())

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self._db.get(User, user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self._db.scalar(stmt)

    def create(self, user: User) -> User:
        self._db.add(user)
        return user