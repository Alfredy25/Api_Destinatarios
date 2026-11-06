from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class CoverageType(str, Enum):
    PAQUETEXPRESS = "PAQUETEXPRESS"
    ZONA_PLUS = "ZONA PLUS"
    ZONA_PLUS_ESPECIAL = "ZONA PLUS ESPECIAL"


class CoveragePxDto(BaseModel):
    id_delivery: int
    postal_code: str = Field(default=None, description="clave codigo postal entre 4 y 5 caracteres.")
    colony: str = Field(default=None, description="Colonia o Asentamiento")
    municipality: str = Field(default=None, description="Delegación o Municipio")
    city: str = Field(default=None, description="Ciudad")
    state: str = Field(default=None, description="Estado de la republica Méxicana")
    coverage_type: CoverageType

    model_config = ConfigDict(from_attributes=True)


class CoveragePxRequest(BaseModel):
    id_delivery: int | None = None
    branch: str = Field(...)
    place: str = Field(...)
    postal_code: str = Field(..., min_length=4, max_length=5,
                             description="clave codigo postal entre 4 y 5 caracteres.")
    colony: str = Field(..., min_length=3, max_length=60,
                        description="Colonia o Asentamiento")
    municipality: str = Field(..., min_length=3, max_length=50,
                              description="Delegación o Municipio")
    city: str = Field(..., min_length=3, max_length=60,
                      description="Ciudad")
    state: str = Field(..., min_length=4, max_length=60,
                       description="Estado de la republica Méxicana")
    coverage_type: CoverageType
