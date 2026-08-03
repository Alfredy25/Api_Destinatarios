from datetime import datetime

from typing import List, Optional

from fastapi import APIRouter, Body, Depends, Query, status

from app.dependencies.di import get_shipping_service
from app.dependencies.security import get_current_user
from app.entities.user import User
from app.schemas.shipping_dto import ShippingDto
from app.schemas.shipping_request import ShippingRequest
from app.services.shipment_service import ShippingPxService

router = APIRouter(prefix="/shipments-px", tags=["shipments-px"])

@router.get("/", response_model=List[ShippingDto])
def get_shipments(fecha_inicio: Optional[datetime] = Query(default=None, description="Fecha inicial para filtrar envíos por fecha de creación"),
                  fecha_fin: Optional[datetime] = Query(default=None, description="Fecha final para filtrar envíos por fecha de creación"),
                  service: ShippingPxService = Depends(get_shipping_service),
                  current_user: User = Depends(get_current_user)):

    return service.list_shipments(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)


@router.post("/", response_model=ShippingDto, status_code=status.HTTP_201_CREATED)
def create_shipment(shipping: ShippingRequest = Body(...),
                    service: ShippingPxService = Depends(get_shipping_service),
                    current_user: User = Depends(get_current_user)):

    return service.create_shipping(shipping=shipping, user=current_user)


@router.get("/{folio}", response_model=ShippingDto)
def get_shipment_by_folio(folio: int, service: ShippingPxService = Depends(get_shipping_service),
                          current_user: User = Depends(get_current_user)):

    return service.find_by_folio(folio)