"""di significa inyección de dependencias"""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.db import SessionLocal

from app.api.v1.record.repository import SQLAlchemyRegisterRepository, RegistroRepository
from app.api.v1.shipment.repository import SQLAlchemyShipmentPxRepository, ShipmentPxRepository
from app.api.v1.user.repository import SQLAlchemyUserRepository, UserRepository
from app.api.v1.coverage_px.repository import CoverageRepository
from app.api.v1.coverage_px.repository import SQLAlchemyCoveragePXRepository

from app.api.v1.record.service import RegistroServiceImpl
from app.api.v1.shipment.service import ShippingPxServiceImpl
from app.api.v1.user.service import UserServiceImpl
from app.api.v1.coverage_px.service import CoveragePxServiceImpl


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


