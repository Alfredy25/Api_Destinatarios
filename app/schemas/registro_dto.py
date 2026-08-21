from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# Salida base del registro
class RegistroDto(BaseModel):
    id: int = Field(..., examples=[1, 2])
    sede: str = Field(..., examples=["AJUSCO", "COYOACAN"])
    nombre_imagen: str = Field(...,  examples=["IMAGEN.JPG"])
    destinatario_raw: str = Field(..., examples=["C. JONH DOE HERNANDEZ PRESIDENTE MUNICIPAL DE HOLA MUNDO DEL ESTADO DE MÉXICO PLAZA DE LA BANDERA, S/N, CENTRO, C.P. 50000, HOLA MUNDO, ESTADO DE MÉXICO. TELÉFONO: (55) 0000 1111"])
    created_at: datetime
    nombre_titulo: Optional[str] = Field(default=None, examples=["C. JOHN DOE PEREZ FERNANDEZ"])
    cargo_dependencia: Optional[str] = Field(default=None, examples=["PRESIDENTE MUNICIPAL DE HOLA MUNDO DEL ESTADO DE MÉXICO"])
    direccion: Optional[str] = Field(default=None, examples=["PRESIDENCIA MUNICIPAL PLAZA DE LA BANDERA, S/N"])
    colonia: Optional[str] = Field(default=None, examples=["CENTRO"])
    municipio_alcaldia: Optional[str] = Field(default=None, examples=["HOLA MUNDO"])
    estado: Optional[str] = Field(default=None, examples=["ESTADO DE MEXICO"])
    codigo_postal: Optional[str] = Field(default=None, examples=["50000"])
    numero_volante: Optional[str] = Field(default=None, examples=["VCS-12-100000-00001"])
    extras: Optional[str] = None
    contacto: Optional[str] = Field(default=None, examples=["TELÉFONO: (55) 0000 1111"])
    indicaciones: Optional[str] = Field(default=None, examples=["FAVOR DE ENTREGAR DE LUNES A VIERNES DE 9:00 A 15:00 HRS"])
    observaciones_ia: Optional[str] = Field(default=None, examples=["LA IMAGEN ESTA LIGERAMENTE BORROSA, PERO EL TEXTO ES LEGIBLE."])

    model_config = ConfigDict(from_attributes=True)


class RegistroDtoUpdate(BaseModel):
    sede: Optional[Literal["AJUSCO", "COYOACAN"]] = None

    nombre_titulo: Optional[str] = None
    cargo_dependencia: Optional[str] = None
    direccion: Optional[str] = None
    colonia: Optional[str] = None
    municipio_alcaldia: Optional[str] = None
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None

    extras: Optional[str] = None
    contacto: Optional[str] = None
    indicaciones: Optional[str] = None
    observaciones_ia: Optional[str] = None



