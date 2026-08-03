from decimal import Decimal
from app.entities.user import User
from sqlalchemy import Integer, String, Text, Numeric, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy.sql import func

class ShipmentPx(Base):
    __tablename__ = "shipments_px"
    id_shipping: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_receiver: Mapped[str] = mapped_column(String(100), nullable=False)
    id_folio: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True, unique=True)
    rfc: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    colony: Mapped[str] = mapped_column(String(100), nullable=False)
    street: Mapped[str] = mapped_column(String(100), nullable=False)
    num_street: Mapped[str] = mapped_column(String(50), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(10), nullable=False)
    email: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    address_reference: Mapped[str | None] = mapped_column(Text, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    package_code: Mapped[int] = mapped_column(TINYINT(unsigned=True), nullable=False)
    content: Mapped[str] = mapped_column(String(100), nullable=False)
    weight: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable = False)
    length: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable = False)
    width: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable = False)
    height: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable = False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    # Desde Shipment se puede acceder al user
    created_by_user: Mapped["User"] = relationship("User")

    def __repr__(self) -> str:
        attrs = [
            f"id_shipping={self.id_shipping!r}",
            f"id_folio={self.id_folio!r}",
            f"name_receiver={self.name_receiver!r}",
            f"rfc={self.rfc!r}",
            f"country={self.country!r}",
            f"state={self.state!r}",
            f"city={self.city!r}",
            f"colony={self.colony!r}",
            f"street={self.street!r}",
            f"num_street={self.num_street!r}",
            f"postal_code={self.postal_code!r}",
            f"email={self.email!r}",
            f"phone={self.phone!r}",
            f"address_reference={self.address_reference!r}",
            f"quantity={self.quantity!r}",
            f"package_code={self.package_code!r}",
            f"content={self.content!r}",
            f"weight={self.weight!r}",
            f"length={self.length!r}",
            f"width={self.width!r}",
            f"height={self.height!r}",
            f"created_at={self.created_at!r}",
            f"created_by={self.created_by!r}",
        ]

        return f"ShipmentPx({', '.join(attrs)})"
