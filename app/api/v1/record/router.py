from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, Body, status
from app.core.dependencies import get_register_service
from app.api.v1.security.service import get_current_user
from app.entities.user import User
from app.api.v1.record.schemas import RegistroDto, RegistroDtoUpdate, RegistroRequest
from app.api.v1.record.service import RegistroService

router = APIRouter(prefix="/registros", tags=["registros"])

@router.get("/", response_model=List[RegistroDto])
def get_registers(
    sede: Optional[str] = Query(None, examples=["AJUSCO","COYOACAN"]),
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    service: RegistroService = Depends(get_register_service),
    usuario_actual: User = Depends(get_current_user)):

    return service.listar_registros(
        sede=sede, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)


@router.put("/{registro_id}", response_model=RegistroDto)
def update_registration(registro_id: int, registro: RegistroDtoUpdate,
                        service: RegistroService = Depends(get_register_service),
                        usuario_actual: User = Depends(get_current_user)):

    return service.update_registro(registro_id, registro, usuario_actual)


@router.post("/",response_model=RegistroDto, status_code=status.HTTP_201_CREATED)
def create_registration(registro: RegistroRequest = Body(...),
                            service: RegistroService = Depends(get_register_service),
                            user: User = Depends(get_current_user)):
    return service.create_recipient_record(registro, user)

