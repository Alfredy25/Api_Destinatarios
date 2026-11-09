from typing import Annotated

from fastapi import APIRouter, Depends, Path

from app.api.v1.security.service import get_current_user
from app.api.v1.sepomex.schemas import SepomexDto
from app.api.v1.sepomex.service import SepomexService
from app.core.dependencies import get_sepomex_service
from app.entities.user import User

router = APIRouter(prefix="/sepomex", tags=["sepomex"])


@router.get("/{postal_code}", response_model=list[SepomexDto])
def get_by_postal_code(
    postal_code: Annotated[
        str,
        Path(
            pattern=r"^\d{5}$",
            description="Código postal de 5 dígitos",
            examples=["97000"],
        ),
    ],
    service: SepomexService = Depends(get_sepomex_service),
    current_user: User = Depends(get_current_user),
) -> list[SepomexDto]:
    """Consulta los asentamientos de un código postal."""
    return service.get_by_postal_code(postal_code)
