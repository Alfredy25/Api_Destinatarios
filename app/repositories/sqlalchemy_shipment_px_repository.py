from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.entities.shipment_px import ShipmentPx
from app.repositories.shipment_px_repository import ShipmentPxRepository
from app.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository


class SQLAlchemyShipmentPxRepository(ShipmentPxRepository):

    def __init__(self, db: Session):
        self._db = db

    def find_all(self, fecha_inicio: Optional[datetime] = None,
                 fecha_fin: Optional[datetime] = None) -> List[ShipmentPx]:

        stmt = select(ShipmentPx)
        if fecha_inicio:
            stmt = stmt.where(ShipmentPx.created_at >= fecha_inicio)
        if fecha_fin:
            stmt = stmt.where(ShipmentPx.created_at <= fecha_fin)

        stmt = stmt.order_by(ShipmentPx.created_at.desc())

        result = self._db.execute(stmt)

        return list(result.scalars().all())

    def create(self, shipping: ShipmentPx) -> ShipmentPx:
        self._db.add(shipping)
        # Ejecuta INSERT para que MySQL genere id_shipping
        self._db.flush()
        shipping.id_folio = shipping.id_shipping
        return shipping

    def find_by_id(self, shipping_id: int) -> ShipmentPx | None:
        return self._db.get(ShipmentPx, shipping_id)

    def find_by_folio(self, folio: int) -> ShipmentPx | None:
        stmt = select(ShipmentPx).where(ShipmentPx.id_folio == folio)
        return self._db.scalars(stmt).first()




