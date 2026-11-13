from datetime import datetime
from typing import List, Literal, Optional
import re
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.api.v1.address.schemas import replace_special_characters


NAME_ABBREVIATIONS = {
    "ADMINISTRADORA DESCONCENTRADA DE RECAUDACION": "ADM. DESC. DE REC.",
    "ADMINISTRADOR DESCONCENTRADA DE RECAUDACION": "ADM. DESC. DE REC.",
    "BAJA CALIFORNIA SUR": "B.C.S.",
    "SAN LUIS POTOSI": "S.L.P.",
    "ESTADO": "EDO",
    "ADMINISTRADORA": "ADMIN.",
    "ADMINISTRADOR": "ADMIN.",
    "ADMINISTRACION": "ADMON.",
    "PRESIDENTA": "PDTA.",
    "PRESIDENTE": "PDTE.",
    "DIRECTORA": "DIR.A",
    "DIRECTOR": "DIR.",
    "SECRETARIA": "SECRET.A",
    "SECRETARIO": "SEC.",
    "GOBERNADOR": "GOB.",
    "UNIVERSIDAD": "UNI",
    "AUTONOMA": "AUT.",
    "MAESTRA": "MTRA.",
    "MAESTRO": "MTRO.",
    "PROFESORA": "PROFA.",
    "PROFESOR": "PROF.",
    "DIPUTADA": "DIP.",
    "DIPUTADO": "DIP.",
    "SENADORA": "SEN.",
    "SENADOR": "SEN.",
    "DOCTORA": "DRA.",
    "DOCTOR": "DR.",
    "TITULAR": "TIT.",
    "GENERAL": "GRAL.",
}


def replace_whole_words(value: str) -> str:
    words = sorted(
        NAME_ABBREVIATIONS,
        key=len,
        reverse=True,
    )

    regex = r"\b(?:{})\b".format(
        "|".join(
            re.escape(word)
            for word in words
        )
    )

    pattern = re.compile(regex)

    text = pattern.sub(
        lambda match: NAME_ABBREVIATIONS[match.group(0)],
        value
    )

    return replace_special_characters(text)




def normalize_abbreviation(value: object) -> object:
    if isinstance(value, str):
        return replace_whole_words(value.strip().upper()) 
    return value


def normalize_meaning(value: object) -> object:
    if isinstance(value, str):
        return value.strip().title()
    return value


class JobDto(BaseModel):
    id: int
    abbreviation: str
    meaning: str
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class JobCreate(BaseModel):
    abbreviation: str = Field(
        ...,
        min_length=2,
        max_length=60,
        examples=["DIR."],
        description="Abreviatura del cargo",
        pattern=r"^[A-Za-záéíóúÁÉÍÓÚñÑ0-9. ]+$",
    )
    meaning: str = Field(
        ...,
        min_length=3,
        max_length=150,
        examples=["Director"],
        description="Significado de la abreviatura",
        pattern=r"^[A-Za-záéíóúÁÉÍÓÚñÑ0-9 ]+$",
    )

    @field_validator("abbreviation", mode="before")
    @classmethod
    def normalize_abbreviation_field(cls, value: object) -> object:
        return normalize_abbreviation(value)

    @field_validator("meaning", mode="before")
    @classmethod
    def normalize_meaning_field(cls, value: object) -> object:
        return normalize_meaning(value)


class JobUpdate(BaseModel):
    abbreviation: Optional[str] = Field(default=None, min_length=2, max_length=60, pattern=r"^[A-Za-zñÑ. ]+$",examples=["DIR. GRAL."])
    meaning: Optional[str] = Field(default=None, min_length=3, max_length=150, pattern=r"^[A-Za-záéíóúÁÉÍÓÚñÑ ]+$", examples=["Director General"])

    @field_validator("abbreviation", mode="before")
    @classmethod
    def normalize_abbreviation_field(cls, value: object) -> object:
        if value is None:
            raise ValueError("La abreviatura no puede ser nula")
        return normalize_abbreviation(value)

    @field_validator("meaning", mode="before")
    @classmethod
    def normalize_meaning_field(cls, value: object) -> object:
        if value is None:
            raise ValueError("El significado no puede ser nulo")
        return normalize_meaning(value)


class PaginatedJobs(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    order_by: Literal["id", "abbreviation", "meaning"]
    direction: Literal["desc", "asc"]
    search: Optional[str] = None
    items: List[JobDto] = Field(default_factory=list)


class TotalsJobs(BaseModel):
    total: int
    total_pages: int
    current_page: int
    offset: int

    model_config = ConfigDict(from_attributes=True)
