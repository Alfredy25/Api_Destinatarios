from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ShippingRequest(BaseModel):
    name_receiver: str = Field(..., min_length=4, max_length=80,
        examples=["DR. PEPE PINEDO PINEDO"])

    rfc: str = Field(..., min_length=12, max_length=15,
        examples=["XAXX-010101-000"])

    country: str = Field(..., min_length=3,max_length=50,
        examples=["MEXICO"])

    state: str = Field(..., min_length=5, max_length=50,
        examples=["ZACATECAS"])

    city: str = Field(..., min_length=3, max_length=60,
        examples=["CIUDAD GOBIERNO"])

    colony: str = Field(..., min_length=3, max_length=60,
        examples=["COLONIA JUAREZ"])

    street: str = Field(..., min_length=3, max_length=80,
        examples=["CTO. CERRO DEL GATO"])

    num_street: str = Field(..., min_length=1, max_length=15,
        examples=["SN", "123"])

    postal_code: str = Field(..., min_length=4, max_length=5,
        pattern=r"^[0-9]+$", examples=["98160"])

    email: Optional[EmailStr] = Field(default=None,
        max_length=80, examples=["destinatario@example.com"])

    phone: Optional[str] = Field(default=None, min_length=10, max_length=20,
        examples=["5555555555"])

    address_reference: Optional[str] = Field(default=None, max_length=50,
        examples=["Edificio G, cerca de la entrada principal."])

    quantity: int = Field(..., ge=1, examples=[1])

    package_code: int = Field(..., ge=1, le=63, examples=[1])

    content: str = Field(..., min_length=10, max_length=100,
        examples=["Documentos Legales"])

    weight: Decimal = Field(..., gt=0, max_digits=8,
        decimal_places=2, examples=["1.00"])

    length: Decimal = Field(..., gt=0, max_digits=8,
        decimal_places=2, examples=["30.00"])

    width: Decimal = Field(..., gt=0, max_digits=8,
        decimal_places=2, examples=["20.00"])

    height: Decimal = Field(..., gt=0, max_digits=8,
        decimal_places=2, examples=["10.00"])