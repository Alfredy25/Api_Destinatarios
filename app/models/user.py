from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.db.base import Base

# -----------------------------------------------------------------------------
# Modelo: User
# -----------------------------------------------------------------------------
# Representa a los usuarios del sistema.
# Se utiliza para:
# - Autenticación (login / JWT)
# - Auditoría (created_by, updated_by)
#
# IMPORTANTE:
# - NO almacenamos contraseñas en texto plano
# - password_hash contendrá el hash bcrypt (más adelante)
# -----------------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    # Identificador único del usuario
    id = Column(Integer, primary_key=True, index=True)

    # Nombre de usuario (único)
    username = Column(String(100), unique=True, nullable=False, index=True)

    # Hash de la contraseña (bcrypt)
    # Nunca se guarda la contraseña en claro
    password_hash = Column(String(255), nullable=False)

    # Indica si el usuario está activo o deshabilitado
    # Permite soft-disable sin borrar registros históricos
    is_active = Column(Boolean, default=True, nullable=False)

    # Fecha de creación del usuario
    # Generada automáticamente por la base de datos
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
