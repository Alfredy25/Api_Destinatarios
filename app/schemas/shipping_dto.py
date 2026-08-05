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
    coverage_type: str = Field(default=None, examples=["PAQUETEXPRESS"])

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)