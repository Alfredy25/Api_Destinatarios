import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# -----------------------------------------------------------------------------
# Cargamos variables de entorno desde el archivo .env
# -----------------------------------------------------------------------------
# Esto permite acceder a credenciales sin hardcodearlas en el código
# -----------------------------------------------------------------------------
load_dotenv()

# -----------------------------------------------------------------------------
# Leemos variables de entorno necesarias para la BD
# -----------------------------------------------------------------------------
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# -----------------------------------------------------------------------------
# Construcción de la URL de conexión para MySQL usando PyMySQL
# -----------------------------------------------------------------------------
# Formato:
# mysql+pymysql://usuario:password@host:puerto/base_de_datos
# -----------------------------------------------------------------------------
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# -----------------------------------------------------------------------------
# Engine SQLAlchemy
# -----------------------------------------------------------------------------
# pool_pre_ping:
#   - Evita errores cuando MySQL cierra conexiones inactivas
# -----------------------------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# -----------------------------------------------------------------------------
# SessionLocal:
# - Cada request usará su propia sesión
# - autoflush=False y autocommit=False son buenas prácticas
# -----------------------------------------------------------------------------
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
)

# -----------------------------------------------------------------------------
# Dependency para FastAPI
# -----------------------------------------------------------------------------
# Se usará con Depends(get_db) en los endpoints
# -----------------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Prueba de conexión
if __name__ == "__main__":
    try:
        connection = engine.connect()
        print("Conexión a la base de datos exitosa")
        connection.close()
    except Exception as e:
        print("Error al conectar a la base de datos:")
        print(e)