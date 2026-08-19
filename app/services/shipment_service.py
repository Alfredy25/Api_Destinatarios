from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List

from app.entities.user import User
from app.schemas.shipping_dto import ShippingDto, ShippingDtoUpdate
from app.schemas.shipping_request import ShippingRequest


class ShippingPxService(ABC):

    @abstractmethod
    def list_shipments(self, fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None) -> List[ShippingDto]:
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