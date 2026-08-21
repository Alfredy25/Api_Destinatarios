"""
Un service representa una capa donde colocas la lógica de aplicación o lógica de negocio.
Un Service es un componente con comportamiento/lógica.
Service = lógica / acciones / casos de uso

Por ejemplo, el service podría encargarse de:
    - Buscar mensaje por ID.

"""
from abc import ABC, abstractmethod
from typing import List
from app.schemas.coverage_px_dto import CoveragePxDto


class CoverageService(ABC):

    @abstractmethod
    def find_by_cp(self, postal_code: str) -> List[CoveragePxDto | None]:
        ...