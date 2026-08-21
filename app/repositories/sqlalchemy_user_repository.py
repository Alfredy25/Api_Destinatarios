from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.entities.user import User
from app.repositories.user_repository import UserRepository


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