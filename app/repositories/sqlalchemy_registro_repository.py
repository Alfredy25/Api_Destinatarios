from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime
from app.entities import RegistroDestinatario
from app.repositories.registro_repository import RegistroRepository


class SQLAlchemyRegisterRepository(RegistroRepository):

    def __init__(self, db: Session):
        self._db = db

    def find_all(self, sede: Optional[str] = None,
                 fecha_inicio: Optional[datetime] = None,
                 fecha_fin: Optional[datetime] = None) -> List[RegistroDestinatario]:

        stmt = select(RegistroDestinatario)
        if sede:
            stmt = stmt.where(RegistroDestinatario.sede == sede)
        if fecha_inicio:
            stmt = stmt.where(RegistroDestinatario.created_at >= fecha_inicio)
        if fecha_fin:
            stmt = stmt.where(RegistroDestinatario.created_at <= fecha_fin)

        stmt = stmt.order_by(RegistroDestinatario.created_at.desc())

        result = self._db.execute(stmt)

        return list(result.scalars().all())


    def create(self, registro: RegistroDestinatario) -> RegistroDestinatario:
        self._db.add(registro)
        return registro

    def find_by_id(self, registro_id: int) -> Optional[RegistroDestinatario]:
        return self._db.get(RegistroDestinatario, registro_id)

    def find_by_name_image(self, name_image: str) -> Optional[RegistroDestinatario]:
        stmt = select(RegistroDestinatario).where(RegistroDestinatario.nombre_imagen == name_image)
        return self._db.scalars(stmt).first()