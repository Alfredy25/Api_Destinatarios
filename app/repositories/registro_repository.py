from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List

from app.entities.registro import RegistroDestinatario

class RegistroRepository(ABC):

    def find_all(self, sede: Optional[str] = None,
                 fecha_inicio: Optional[datetime] = None,
                 fecha_fin: Optional[datetime] = None) -> List[RegistroDestinatario]:
        ...

    @abstractmethod
    def create(self, user: RegistroDestinatario) -> RegistroDestinatario:
        ...


    @abstractmethod
    def find_by_id(self, registro_id: int) -> RegistroDestinatario:
        ...

    @abstractmethod
    def find_by_name_image(self, name_image: str) -> Optional[RegistroDestinatario]:
        ...