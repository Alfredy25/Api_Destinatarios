from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Enum,
    DateTime,
    ForeignKey,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base

# -----------------------------------------------------------------------------
# Modelo: RegistroDestinatario
# -----------------------------------------------------------------------------
# Representa un sobre procesado por OCR y revisado por un operador.
#
# Incluye:
# - Datos textuales OCR y validados
# - Datos geométricos del recorte de imagen
# - Auditoría completa (created_by / updated_by)
#
# NOTA:
# FastAPI y Pydantic se encargarán de la validación
# SQLAlchemy solo persiste la estructura
# -----------------------------------------------------------------------------
class RegistroDestinatario(Base):
    __tablename__ = "registros_destinatarios"

    # Identificador principal
    id = Column(Integer, primary_key=True, index=True)

    # Origen físico del sobre
    sede = Column(
        Enum("AJUSCO", "COYOACAN", name="sede_enum"),
        nullable=False,
        index=True
    )

    # Información de la imagen
    nombre_imagen = Column(String(255), nullable=False)

    # Texto OCR sin procesar (raw)
    destinatario_raw = Column(Text, nullable=False)

    # Campos estructurados después de revisión humana
    nombre_o_titulo = Column(String(255))
    cargo_dependencia = Column(String(255))
    direccion = Column(String(255))
    colonia = Column(String(255))
    municipio_o_alcaldia = Column(String(255))
    estado = Column(String(255))
    codigo_postal = Column(String(6))

    # Información adicional
    extras = Column(Text)
    contacto = Column(String(255))
    indicaciones = Column(Text)

    # Observaciones generadas por IA
    observaciones_ia = Column(Text)

    # Información geométrica del recorte OCR
    crop_x = Column(Integer)
    crop_y = Column(Integer)
    crop_w = Column(Integer)
    crop_h = Column(Integer)
    rotation_deg = Column(Integer)

    aspect_mode = Column(
        Enum("FREE", "SQUARE", name="aspect_mode_enum"),
        nullable=False
    )

    # Auditoría temporal
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Auditoría de usuarios
    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    updated_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # Relaciones ORM
    created_by_user = relationship(
        "User",
        foreign_keys=[created_by],
        lazy="joined"
    )

    updated_by_user = relationship(
        "User",
        foreign_keys=[updated_by],
        lazy="joined"
    )