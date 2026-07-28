from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException, status

from app.dependencies.di import get_coverage_service
from app.dependencies.security import get_current_user
from app.entities import User
from app.schemas.coverage_px_dto import CoveragePxDto
from app.services.coverage_service import CoverageService

router = APIRouter(prefix="/coverages", tags=["coverages_px"])


@router.get("/", response_model=List[CoveragePxDto])
def lis_coverages_by_cp(postal_code: str = Query(..., alias="cp"),
        service: CoverageService = Depends(get_coverage_service),
                        current_user: User = Depends(get_current_user)):

    coverages = service.find_by_cp(postal_code)
    if not coverages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no hay cobertura con el cp {postal_code} en el sistema"
            )
    return coverages