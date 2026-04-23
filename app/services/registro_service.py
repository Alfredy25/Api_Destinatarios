from fastapi import HTTPException, status
from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.registro import RegistroDestinatario
from app.schemas.registro import RegistroCreate
from app.models.user import User


# Crear un registro de destinatario
# Este servicio:
    # - Recibe datos validados por Pydantic
    # - Asigna automáticamente auditoría (created_by / updated_by)
    # - Persiste el registro en la base de datos
def crear_registro(
    db: Session,
    data: RegistroCreate,
    usuario_actual: User,
) -> RegistroDestinatario:
    registro = RegistroDestinatario(
        **data.model_dump(),
        created_by=usuario_actual.id,
        updated_by=usuario_actual.id,
    )

    db.add(registro)
    db.commit()
    db.refresh(registro)

    return registro



# Listar registros con filtros opcionales
# -----------------------------------------------------------------------------
def listar_registros(
    db: Session,
    sede: Optional[str] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
) -> List[RegistroDestinatario]:

    query = db.query(RegistroDestinatario)
    filtros = []

    if sede:
        filtros.append(RegistroDestinatario.sede == sede)

    if fecha_inicio:
        filtros.append(RegistroDestinatario.created_at >= fecha_inicio)

    if fecha_fin:
        filtros.append(RegistroDestinatario.created_at <= fecha_fin)

    if filtros:
        query = query.filter(and_(*filtros))

    return query.order_by(RegistroDestinatario.created_at.desc()).all()


# Actualizar un registro existente
# -----------------------------------------------------------------------------
def actualizar_registro(
    db: Session,
    registro_id: int,
    data,
    usuario_actual: User,
) -> RegistroDestinatario:
    registro = (
        db.query(RegistroDestinatario)
        .filter(RegistroDestinatario.id == registro_id)
        .first()
    )

    if not registro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro no encontrado",
        )

    # Actualización parcial: solo campos enviados
    update_data = data.model_dump(exclude_unset=True)

    for campo, valor in update_data.items():
        setattr(registro, campo, valor)

    # Auditoría
    registro.updated_by = usuario_actual.id

    db.commit()
    db.refresh(registro)

    return registro
