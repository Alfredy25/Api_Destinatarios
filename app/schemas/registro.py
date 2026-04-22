from typing import Optional, Literal
from datetime import datetime

from pyasn1.type.namedtype import OptionalNamedType
from pydantic import BaseModel, Field


# Schema base compartido
# -----------------------------------------------------------------------------
class RegistroBase(BaseModel):
    sede: Literal["AJUSCO", "COYOACAN"]

    nombre_imagen: str
    destinatario_raw: str

    nombre_o_titulo: Optional[str] = None
    cargo_dependencia: Optional[str] = None
    direccion: Optional[str] = None
    colonia: Optional[str] = None
    municipio_o_alcaldia: Optional[str] = None
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None

    extras: Optional[str] = None
    contacto: Optional[str] = None
    indicaciones: Optional[str] = None
    observaciones_ia: Optional[str] = None

    crop_x: Optional[int] = None
    crop_y: Optional[int] = None
    crop_w: Optional[int] = None
    crop_h: Optional[int] = None
    rotation_deg: Optional[int] = None

    aspect_mode: Literal["FREE", "SQUARE"]


# Schema: RegistroCreate
# -----------------------------------------------------------------------------
# Entrada al crear un registro OCR
class RegistroCreate(RegistroBase):
    pass


# Schema: RegistroUpdate
# -----------------------------------------------------------------------------
# Entrada para actualización parcial
# Todos los campos son opcionales
class RegistroUpdate(BaseModel):
    sede: Optional[Literal["AJUSCO", "COYOACAN"]] = None

    nombre_o_titulo: Optional[str] = None
    cargo_dependencia: Optional[str] = None
    direccion: Optional[str] = None
    colonia: Optional[str] = None
    municipio_o_alcaldia: Optional[str] = None
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None

    extras: Optional[str] = None
    contacto: Optional[str] = None
    indicaciones: Optional[str] = None
    observaciones_ia: Optional[str] = None

    crop_x: Optional[int] = None
    crop_y: Optional[int] = None
    crop_w: Optional[int] = None
    crop_h: Optional[int] = None
    rotation_deg: Optional[int] = None

    aspect_mode: Optional[Literal["FREE", "SQUARE"]] = None


# Schema: RegistroRead
# -----------------------------------------------------------------------------
# Salida oficial de la API
class RegistroRead(RegistroBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: int

    class Config:
        from_attributes = True


