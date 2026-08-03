from datetime import datetime
from typing import Optional, List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.entities.shipment_px import ShipmentPx
from app.entities.user import User
from app.repositories.shipment_px_repository import ShipmentPxRepository
from app.schemas.shipping_dto import ShippingDto
from app.schemas.shipping_request import ShippingRequest
from app.services.shipment_service import ShippingPxService


class ShippingPxServiceImpl(ShippingPxService):

    def __init__(self, repo: ShipmentPxRepository, db: Session):
        self._repo = repo
        self._db = db

    def list_shipments(self, fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None) -> List[ShippingDto]:

        now = datetime.today()

        if fecha_inicio is None and fecha_fin is None:
            fecha_inicio = datetime(year=now.year, month=now.month, day=now.day,
                                    hour=0, minute=0, second=0, microsecond=0)
            fecha_fin = now
        elif fecha_inicio is None and fecha_fin is not None:
            fecha_inicio = fecha_fin.replace(hour=0, minute=0, second=0, microsecond=0)
        elif fecha_inicio is not None and fecha_fin is None:
            fecha_fin = now

        if fecha_inicio > now or fecha_fin > now:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="La fecha inicio o fecha fin no puede ser mayor a la fecha actual")

        if fecha_inicio > fecha_fin:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="La fecha inicio no puede ser mayor que la fecha fin")

        shipment_entities = self._repo.find_all(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

        return [ShippingDto.model_validate(shipment)
            for shipment in shipment_entities]

    def create_shipping(self, shipping: ShippingRequest, user: User) -> ShippingDto:

        shipment_entity = ShipmentPx(
            name_receiver=shipping.name_receiver.upper(),
            rfc=shipping.rfc.upper(),
            country=shipping.country.upper(),
            state=shipping.state.upper(),
            city=shipping.city.upper(),
            colony=shipping.colony.upper(),
            street=shipping.street.upper(),
            num_street=shipping.num_street.upper(),
            postal_code=shipping.postal_code,
            email=str(shipping.email) if shipping.email else None,
            phone=shipping.phone if shipping.phone else None,
            address_reference=shipping.address_reference.upper() if shipping.address_reference else None,
            quantity=shipping.quantity,
            package_code=shipping.package_code,
            content=shipping.content.upper(),
            weight=shipping.weight,
            length=shipping.length,
            width=shipping.width,
            height=shipping.height,
            created_by=user.id
        )

        try:
            self._repo.create(shipment_entity)

            self._db.commit()
            self._db.refresh(shipment_entity)

            return ShippingDto.model_validate(shipment_entity)

        except Exception:
            self._db.rollback()
            raise

    def find_by_folio(self, folio: int) -> Optional[ShippingDto]:
        shipment_entity = self._repo.find_by_folio(folio)
        if not shipment_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail="Envío no encontrado")

        return ShippingDto.model_validate(shipment_entity)
