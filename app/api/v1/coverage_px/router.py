from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException, status

from app.api.v1.coverage_px.schemas import CoveragePxDto
from app.api.v1.coverage_px.service import CoverageService
from app.core.dependencies import get_coverage_service
from app.api.v1.security.service import get_current_user
from app.entities import User


router = APIRouter(prefix="/coverages", tags=["coverages_px"])


@router.get("/", response_model=List[CoveragePxDto])
def list_coverages_by_cp(postal_code: str = Query(..., min_length=4, alias="cp", max_length=5),
        service: CoverageService = Depends(get_coverage_service),
                        current_user: User = Depends(get_current_user)):

    coverages = service.find_by_cp(postal_code)
    if not coverages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no hay cobertura con el cp {postal_code} en el sistema"
            )
    return coverages