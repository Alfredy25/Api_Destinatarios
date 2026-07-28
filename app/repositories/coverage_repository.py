from abc import ABC, abstractmethod
from typing import List

from app.entities.coverage_px import CoveragePX


class CoverageRepository(ABC):

    @abstractmethod
    def find_by_cp(self, coverage_cp: str) -> List[CoveragePX]:
        ...