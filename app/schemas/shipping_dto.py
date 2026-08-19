from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, EmailStr


class ShippingDto(BaseModel):
    id_shipping: int = Field(..., examples=[1])
    id_folio: int = Field(default=..., examples=[1])

    name_receiver: str = Field(..., examples=["DR. LUCAS PINEDO PINEDO"])
    rfc: str = Field(..., examples=["XAXX010101000"])
    country: str = Field(..., examples=["MEXICO"])
    state: str = Field(..., examples=["ZACATECAS"])
    city: str = Field(..., examples=["CIUDAD GOBIERNO"])
    colony: str = Field(..., examples=["LOS ANGELES"])
    street: str = Field(..., examples=["CTO. CERRO DEL GATO"])
    num_street: str = Field(..., examples=["20"])
    postal_code: str = Field(..., examples=["98160"])

    email: Optional[EmailStr] = Field(default=None, examples=["destinatario@example.com"])
    phone: Optional[str] = Field(default=None, examples=["55 5555 5555"])
    address_reference: Optional[str] = Field(default=None)

    quantity: int = Field(..., examples=[1])
    package_code: int = Field(..., examples=[1])
    content: str = Field(..., examples=["Documentos Legales"])

    weight: Decimal = Field(..., examples=["1.00"])
    length: Decimal = Field(..., examples=["30.00"])
    width: Decimal = Field(..., examples=["20.00"])
    height: Decimal = Field(..., examples=["10.00"])
    coverage_type: Optional[str] = Field(default=None, examples=["PAQUETEXPRESS"])
    comments: Optional[str] = Field(default=None, examples=["ENTREGAR EN OFICIALIA DE PARTES O RECEPCION EN UN HORARIO DE 09:00 A 14:00 HRS."])
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ShippingDtoUpdate(BaseModel):
    name_receiver: Optional[str] = Field(default=None, examples=["DR. LUCAS PINEDO PINEDO"])
    rfc: Optional[str] = Field(default=None, examples=["XAXX010101000"])
    country: Optional[str] = Field(default=None, examples=["MEXICO"])
    state: Optional[str] = Field(default=None, examples=["ZACATECAS"])
    city: Optional[str] = Field(default=None, examples=["CIUDAD GOBIERNO"])
    colony: Optional[str] = Field(default=None, examples=["LOS ANGELES"])
    street: Optional[str] = Field(default=None, examples=["CTO. CERRO DEL GATO"])
    num_street: Optional[str] = Field(default=None, examples=["20"])
    postal_code: Optional[str] = Field(default=None, examples=["98160"])

    email: Optional[EmailStr] = Field(default=None, examples=["destinatario@example.com"])
    phone: Optional[str] = Field(default=None, examples=["55 5555 5555"])
    address_reference: Optional[str] = Field(default=None)

    quantity: Optional[int] = Field(default=None, examples=[1])
    package_code: Optional[int] = Field(default=None, examples=[1])
    content: Optional[str] = Field(default=None, examples=["Documentos Legales"])

    weight: Optional[Decimal] = Field(default=None, examples=["1.00"])
    length: Optional[Decimal] = Field(default=None, examples=["30.00"])
    width: Optional[Decimal] = Field(default=None, examples=["20.00"])
    height: Optional[Decimal] = Field(default=None, examples=["10.00"])
    comments: Optional[str] = Field(
        default=None,
        examples=["ENTREGAR EN OFICIALIA DE PARTES O RECEPCION EN UN HORARIO DE 09:00 A 14:00 HRS."],
    )

    model_config = ConfigDict(from_attributes=True)