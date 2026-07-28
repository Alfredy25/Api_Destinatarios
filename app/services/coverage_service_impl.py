from typing import List
from sqlalchemy.orm import Session
from app.schemas.coverage_px_dto import CoveragePxDto

from app.repositories.coverage_repository import CoverageRepository
from app.services.coverage_service import CoverageService


class CoveragePxServiceImpl(CoverageService):
    def __init__(self, repo: CoverageRepository, db: Session):
        self.repo = repo
        self._db = db

    def find_by_cp(self, postal_code: str) -> List[CoveragePxDto]:
        coverages = self.repo.find_by_cp(postal_code)
        return [CoveragePxDto.model_validate(coverage) for coverage in coverages]