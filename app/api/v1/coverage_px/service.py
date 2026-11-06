"""
Un service representa una capa donde colocas la lógica de aplicación o lógica de negocio.
Un Service es un componente con comportamiento/lógica.
Service = lógica / acciones / casos de uso

Por ejemplo, el service podría encargarse de:
    - Buscar mensaje por ID.

"""
from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.orm import Session

from app.api.v1.coverage_px.repository import CoverageRepository
from app.api.v1.coverage_px.schemas import CoveragePxDto


class CoverageService(ABC):

    @abstractmethod
    def find_by_cp(self, postal_code: str) -> List[CoveragePxDto | None]:
        ...


class CoveragePxServiceImpl(CoverageService):
    def __init__(self, repo: CoverageRepository, db: Session):
        self.repo = repo
        self._db = db

    def find_by_cp(self, postal_code: str) -> List[CoveragePxDto]:
        coverages = self.repo.find_by_cp(postal_code)
        return [CoveragePxDto.model_validate(coverage) for coverage in coverages]