from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime

from app.entities.shipment_px import ShipmentPx


class ShipmentPxRepository(ABC):

    @abstractmethod
    def find_all(self, fecha_inicio: Optional[datetime] = None,
                 fecha_fin: Optional[datetime] = None, user_id: int = None) -> List[ShipmentPx]:
        ...

    @abstractmethod
    def create(self, shipment: ShipmentPx) -> ShipmentPx:
        ...

    @abstractmethod
    def find_by_id(self, shipping_id: int) -> ShipmentPx:
        ...

    @abstractmethod
    def find_by_folio(self, folio: int) -> ShipmentPx:
        ...