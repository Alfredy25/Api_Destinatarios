"""di significa inyección de dependencias"""
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.repositories.coverage_repository import CoverageRepository
from app.repositories.registro_repository import RegistroRepository
from app.repositories.shipment_px_repository import ShipmentPxRepository
from app.repositories.sqlalchemy_coverage_repository import SQLAlchemyCoveragePXRepository
from app.repositories.sqlalchemy_registro_repository import SQLAlchemyRegisterRepository
from app.repositories.sqlalchemy_shipment_px_repository import SQLAlchemyShipmentPxRepository
from app.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.repositories.user_repository import UserRepository
from app.services.coverage_service_impl import CoveragePxServiceImpl
from app.services.registro_service_impl import RegistroServiceImpl
from app.services.shipment_service_impl import ShippingPxServiceImpl
from app.services.user_service_impl import UserServiceImpl


# Se usará con Depends(get_db) en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependencias User
def get_user_repository(db: Session = Depends(get_db)):
    return SQLAlchemyUserRepository(db)

def get_user_service(db: Session = Depends(get_db),
                     repository: UserRepository = Depends(get_user_repository)):
    return UserServiceImpl(repository, db)

# Dependencias Registro
def get_registro_repository(db: Session = Depends(get_db)):
    return SQLAlchemyRegisterRepository(db)

def get_register_service(db: Session = Depends(get_db),
                         repository: RegistroRepository = Depends(get_registro_repository)):
    return RegistroServiceImpl(repository, db)

# Dependencias Coverage o Covertura
def get_coverage_px_repository(db: Session = Depends(get_db)):
    return SQLAlchemyCoveragePXRepository(db)

def get_coverage_service(db: Session = Depends(get_db),
                         repository: CoverageRepository = Depends(get_coverage_px_repository)):

    return CoveragePxServiceImpl(repository, db)

# Dependencias Shipment de Paquete Xpress
def get_shipping_repository(db: Session = Depends(get_db)):
    return SQLAlchemyShipmentPxRepository(db)

def get_shipping_service(db: Session = Depends(get_db),
                         repository: ShipmentPxRepository = Depends(get_shipping_repository)):
    return ShippingPxServiceImpl(repository, db)


