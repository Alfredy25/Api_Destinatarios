from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


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




class RegistroRequest(BaseModel):
    sede: Literal["AJUSCO", "COYOACAN"]

    nombre_imagen: str = Field(..., min_length=20, max_length=50, description="nombre de la imagen enviada", examples=["IMG_EXAMPLE.JPG"])
    destinatario_raw: str = Field(...,min_length=40, max_length=660, examples=["C. JONH DOE HERNANDEZ PRESIDENTE MUNICIPAL DE HOLA MUNDO DEL ESTADO DE MÉXICO PLAZA DE LA BANDERA, S/N, CENTRO, C.P. 50000, HOLA MUNDO, ESTADO DE MÉXICO. TELÉFONO: (55) 0000 1111"])

    nombre_titulo: Optional[str] = Field(default=None, max_length=200, examples=["C. JOHN DOE PEREZ FERNANDEZ"])
    cargo_dependencia: Optional[str] = Field(default=None, max_length=255, examples=["PRESIDENTE MUNICIPAL DE HOLA MUNDO DEL ESTADO DE MÉXICO"])
    direccion: Optional[str] = Field(default=None, max_length=255, examples=["PRESIDENCIA MUNICIPAL PLAZA DE LA BANDERA, S/N"])
    colonia: Optional[str] = Field(default=None, max_length=150, examples=["CENTRO"])
    municipio_alcaldia: Optional[str] = Field(default=None, max_length=100, examples=["HOLA MUNDO"])
    estado: Optional[str] = Field(default=None, max_length=100, examples=["ESTADO DE MEXICO"])
    codigo_postal: Optional[str] = Field(default=None, min_length=4, max_length=6, examples=["50000"])

    numero_volante: Optional[str] = Field(default=None, min_length=15, max_length=25, examples=["VCS-12-100000-00001"])
    extras: Optional[str] = Field(default=None, max_length=420)
    contacto: Optional[str] = Field(default=None, max_length=150, examples=["TELÉFONO: (55) 0000 1111"])
    indicaciones: Optional[str] = Field(default=None, max_length=200, examples=["FAVOR DE ENTREGAR DE LUNES A VIERNES DE 9:00 A 15:00 HRS"])

    observaciones_ia: Optional[str] = Field(default=None, max_length=100, examples=["LA IMAGEN ESTA LIGERAMENTE BORROSA, PERO EL TEXTO ES LEGIBLE."])

    crop_x: Optional[int] = Field(default=0, ge=0, examples=[1535])
    crop_y: Optional[int] = Field(default=0, ge=0, examples=[2881])
    crop_w: Optional[int] = Field(default=0, ge=0, examples=[1509])
    crop_h: Optional[int] = Field(default=0, ge=0, examples=[770])

    rotation_deg: Optional[int] = Field(default=0, ge=0, examples=[90, 180, 270, 0])

    aspect_mode: Literal["FREE", "SQUARE"]

