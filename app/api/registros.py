
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.registro import (
    RegistroCreate,
    RegistroRead,
    RegistroUpdate,
)
from app.services.registro_service import (
    crear_registro,
    listar_registros,
    actualizar_registro,
)
from app.core.dependencies import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/registros",
    tags=["registros"],
)

# -----------------------------------------------------------------------------
# Crear nuevo registro de destinatario (OCR)
# -----------------------------------------------------------------------------
# Endpoint protegido:
    # - Requiere JWT válido
    # - Asigna automáticamente created_by y updated_by
@router.post(
    "",
    response_model=RegistroRead,
)
def crear_registro_endpoint(
    data: RegistroCreate,
    db: Session = Depends(get_db),
    usuario_actual: User = Depends(get_current_user),
):
    return crear_registro(
        db=db,
        data=data,
        usuario_actual=usuario_actual,
    )


# GET /registros - Consultar registros (FASE 10)
@router.get("", response_model=List[RegistroRead])
def obtener_registros(
    sede: Optional[str] = Query(None, example="AJUSCO"),
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    usuario_actual: User = Depends(get_current_user),
):
    return listar_registros(
        db=db,
        sede=sede,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )


# PUT /registros/{id} - Actualizar registro OCR
# -----------------------------------------------------------------------------
@router.put("/{registro_id}", response_model=RegistroRead)
def actualizar_registro_endpoint(
    registro_id: int,
    data: RegistroUpdate,
    db: Session = Depends(get_db),
    usuario_actual: User = Depends(get_current_user),
):
    return actualizar_registro(
        db=db,
        registro_id=registro_id,
        data=data,
        usuario_actual=usuario_actual,
    )
