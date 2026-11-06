from abc import ABC, abstractmethod
from app.api.v1.shipment.schemas import ShippingRequest, ShippingDto, ShippingDtoUpdate
from datetime import datetime
from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.entities.shipment_px import ShipmentPx
from app.entities.user import User
from app.api.v1.shipment.repository import ShipmentPxRepository

class ShippingPxService(ABC):

    @abstractmethod
    def list_shipments(self, fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None, user_id: int = None) -> List[ShippingDto]:
        ...

    @abstractmethod
    def create_shipping( self, shipping: ShippingRequest,
                         user: User) -> ShippingDto:
        ...

    @abstractmethod
    def find_by_folio(self, folio: int) -> Optional[ShippingDto]:
        ...

    @abstractmethod
    def update_shipping(self, shipping_id: int, shipping: ShippingDtoUpdate, user: User) -> ShippingDto:
        ...


class ShippingPxServiceImpl(ShippingPxService):

    def __init__(self, repo: ShipmentPxRepository, db: Session):
        self._repo = repo
        self._db = db

    def list_shipments(self, fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None, user_id: int = None) -> List[ShippingDto]:

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


        shipment_entities = self._repo.find_all(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, user_id=user_id if user_id else None)

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
            phone=shipping.phone.upper() if shipping.phone else None,
            address_reference=shipping.address_reference.upper() if shipping.address_reference else None,
            quantity=shipping.quantity,
            package_code=shipping.package_code,
            content=shipping.content.upper(),
            weight=shipping.weight,
            length=shipping.length,
            width=shipping.width,
            height=shipping.height,
            coverage_type=shipping.coverage_type,
            comments=shipping.comments.upper(),
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

    def update_shipping(self, shipping_id: int, shipping: ShippingDtoUpdate,
                        user: User) -> ShippingDto:
        shipping_entity = self._repo.find_by_id(shipping_id)

        if not shipping_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Envio no encontrado')
        update_data = shipping.model_dump(exclude_unset=True)

        for attribute, valor in update_data.items():
            setattr(shipping_entity, attribute, valor)

        shipping_entity.created_by = user.id

        self._db.commit()
        self._db.refresh(shipping_entity)

        return ShippingDto.model_validate(shipping_entity)

