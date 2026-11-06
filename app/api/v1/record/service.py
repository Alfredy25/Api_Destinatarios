from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List

from app.entities import User
from app.api.v1.record.schemas import RegistroRequest, RegistroDto, RegistroDtoUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.entities.registro import RegistroDestinatario
from app.api.v1.record.repository import RegistroRepository


class RegistroService(ABC):

    @abstractmethod
    def listar_registros(self, sede: Optional[str] = None,
                         fecha_inicio: Optional[datetime] = None,
                         fecha_fin: Optional[datetime] = None) -> List[RegistroDto]:
        ...

    @abstractmethod
    def create_recipient_record(self, registro: RegistroRequest, user: User) -> RegistroDto:
        ...

    @abstractmethod
    def update_registro(self, registro_id: int, registro: RegistroDtoUpdate, user: User) -> RegistroDto:
        ...


class RegistroServiceImpl(RegistroService):

    def __init__(self, repo: RegistroRepository, db: Session):
        self._db = db
        self._repo = repo

    def listar_registros(self, sede: Optional[str] = None,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None) -> List[RegistroDto]:

        registros_entities = self._repo.find_all(sede=sede, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

        return [RegistroDto.model_validate(registro) for registro in registros_entities]

    def create_recipient_record(self, registro: RegistroRequest, user: User) -> RegistroDto:

        registro_entity = RegistroDestinatario(
            sede=registro.sede,
            nombre_imagen=registro.nombre_imagen,
            destinatario_raw=registro.destinatario_raw,
            nombre_titulo=registro.nombre_titulo,
            cargo_dependencia=registro.cargo_dependencia,
            direccion=registro.direccion,
            colonia=registro.colonia,
            municipio_alcaldia=registro.municipio_alcaldia,
            estado=registro.estado,
            codigo_postal=registro.codigo_postal,
            numero_volante=registro.numero_volante,
            extras=registro.extras,
            contacto=registro.contacto,
            indicaciones=registro.indicaciones,
            observaciones_ia=registro.observaciones_ia,
            crop_x=registro.crop_x,
            crop_y=registro.crop_y,
            crop_w=registro.crop_w,
            crop_h=registro.crop_h,
            rotation_deg=registro.rotation_deg,
            aspect_mode=registro.aspect_mode,
            created_by=user.id,
            updated_by=user.id
        )
        try:
            self._repo.create(registro_entity)
            self._db.commit()
            self._db.refresh(registro_entity)
            return RegistroDto.model_validate(registro_entity)
        except Exception:
            self._db.rollback()
            raise


    # Actualizar un registro existente
    def update_registro(self, registro_id: int, registro: RegistroDtoUpdate, user: User) -> RegistroDto:

        registro_entity = self._repo.find_by_id(registro_id)

        if not registro_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Registro no encontrado")

        update_data = registro.model_dump(exclude_unset=True)

        for atributo, valor in update_data.items():
            setattr(registro_entity, atributo, valor)

        registro_entity.updated_by = user.id

        self._db.commit()
        self._db.refresh(registro_entity)

        return RegistroDto.model_validate(registro_entity)

