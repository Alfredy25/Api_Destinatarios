from sqlalchemy.orm import declarative_base

# -----------------------------------------------------------------------------
# Base declarativa para todos los modelos SQLAlchemy
# -----------------------------------------------------------------------------
# Todos los modelos del proyecto deben heredar de esta clase
# Esto permite a Alembic detectar automáticamente las tablas
# -----------------------------------------------------------------------------
Base = declarative_base()