from __future__ import annotations
from typing import TYPE_CHECKING
from enum import Enum as PyEnum
from sqlalchemy import (Integer, String, Enum as SQLEnum, ForeignKey,
                        UniqueConstraint, Table, Column)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.core.db import Base
from app.entities.auditable import AuditableMixin

if TYPE_CHECKING:
    from app.entities import PositionORM
    from app.entities import TitleORM
    from app.entities import AddressORM
    from app.entities import ContactORM
    from app.entities import VolanteORM


class EntidadesEnum(str, PyEnum):
    PERSONA = "PERSONA"
    PRIVADA = "PRIVADA"
    GOBIERNO = "GOBIERNO"


receiver_volante = Table(
    "receiver_volante",
    Base.metadata,
    Column("receiver_id", Integer, ForeignKey("receivers.id", ondelete="CASCADE")),
    Column("volante_id", Integer, ForeignKey("volantes.id", ondelete="CASCADE")),
    UniqueConstraint("receiver_id", "volante_id", name="unique_receiver_id"),
)

class ReceiverORM(AuditableMixin, Base):
    __tablename__ = "receivers"
    __table_args__ = (
        UniqueConstraint("full_name", "title_id", "position_id", name="uq_receiver_name_position"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    type_entity: Mapped[str] = mapped_column(SQLEnum(EntidadesEnum, name="entidades_enum"), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(70), nullable=True)
    email: Mapped[str | None] = mapped_column(String(80), nullable=True)

    title_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("titles.id", ondelete="SET NULL"), nullable=True)
    position_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("positions.id", ondelete="SET NULL"), nullable=True)

    title: Mapped["TitleORM"] = relationship("TitleORM", lazy="joined")
    position: Mapped["PositionORM"] = relationship("PositionORM", back_populates="receivers", lazy="joined")
    addresses: Mapped[list["AddressORM"]] = relationship(
        "AddressORM",
        lazy="selectin",
        cascade="all, delete, delete-orphan"
    )
    contacts: Mapped[list["ContactORM"]] = relationship(
        "ContactORM",
        lazy="selectin",
        cascade="all, delete, delete-orphan"
    )

    volantes: Mapped[list["VolanteORM"]] = relationship(
        secondary="receiver_volante",
        back_populates="receivers",
        lazy="select",
        passive_deletes=True,
    )

