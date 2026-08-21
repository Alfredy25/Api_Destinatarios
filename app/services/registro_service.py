from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List

from app.entities import User
from app.schemas.registro_dto import RegistroDto, RegistroDtoUpdate
from app.schemas.registro_request import RegistroRequest


class RegistroService(ABC):

    @abstractmethod
    def listar_registros(self, sede: Optional[str] = None,
                         fecha_inicio: Optional[datetime] = None,
                         fecha_fin: Optional[datetime] = None) -> List[RegistroDto]:
        ...

    @abstractmethod
    def create_recipient_record(self, registro: RegistroRequest, user: User) -> RegistroDto:
        ...

    @abstractmethod
    def update_registro(self, registro_id: int, registro: RegistroDtoUpdate, user: User) -> RegistroDto:
        ...
