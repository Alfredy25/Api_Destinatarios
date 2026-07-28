from datetime import datetime

from sqlalchemy import (Integer, String, Text,
                        Enum, DateTime, ForeignKey)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.database import Base
from app.entities.user import User

class RegistroDestinatario(Base):
    __tablename__ = "registros_destinatarios"

    id: Mapped[int] = mapped_column(Integer,primary_key = True, autoincrement = True, index = True)
    sede: Mapped[str] = mapped_column(Enum("AJUSCO", "COYOACAN", name="sede_enum"),nullable=False, index=True)

    nombre_imagen: Mapped[str] = mapped_column(String(50), nullable=False)
    destinatario_raw: Mapped[str] = mapped_column(Text, nullable=False)


    nombre_titulo: Mapped[str | None] = mapped_column(String(255)) # Renombrada
    cargo_dependencia: Mapped[str | None] = mapped_column(String(255))
    direccion: Mapped[str | None] = mapped_column(String(255))
    colonia: Mapped[str | None] = mapped_column(String(150))
    municipio_alcaldia: Mapped[str | None] = mapped_column(String(255)) # Renombrada
    estado: Mapped[str | None] = mapped_column(String(100))
    codigo_postal: Mapped[str | None] = mapped_column(String(6))

    numero_volante: Mapped[str | None] = mapped_column(String(50)) # Agregada
    extras: Mapped[str | None] = mapped_column(Text)
    contacto: Mapped[str | None] = mapped_column(String(150))
    indicaciones: Mapped[str | None] = mapped_column(String(200))

    observaciones_ia: Mapped[str | None] = mapped_column(String(100))

    crop_x: Mapped[int] = mapped_column(Integer, nullable=False)
    crop_y: Mapped[int] = mapped_column(Integer, nullable=False)
    crop_w: Mapped[int] = mapped_column(Integer, nullable=False)
    crop_h: Mapped[int] = mapped_column(Integer, nullable=False)
    rotation_deg: Mapped[int | None] = mapped_column(Integer)

    aspect_mode: Mapped[str] = mapped_column(Enum("FREE", "SQUARE", name="aspect_mode_enum"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    created_by_user: Mapped["User"] = relationship(
        "User",foreign_keys=[created_by], lazy="joined")
    updated_by_user: Mapped["User"] = relationship(
        "User", foreign_keys=[updated_by], lazy="joined")