from fastapi import FastAPI, Request

from app.middlewares.timing_middleware import timing_middleware

from app.api.v1.coverage_px.router import router as coverage_px_router
from app.api.v1.security.router import router as auth_router
from app.api.v1.record.router import router as records_router
from app.api.v1.user.router import router as users_router
from app.api.v1.shipment.router import router as shipments_px_router
from app.api.v1.address.router import router as address_router
from app.api.v1.contact.router import router as contact_router
from app.api.v1.job_role.router import router as job_role_router
from app.api.v1.organization.router import router as organization_router
from app.api.v1.receiver.router import router as receiver_router
from app.api.v1.title.router import router as title_router
from app.api.v1.sepomex.router import router as sepomex_router
from app.api.v1.volante.router import router as volante_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(
    title="OCR Destinatarios API",
    description="Backend REST para el sistema extractor OCR de destinatarios",
    version="0.1.0"
)


# CORS en producción se deben restringir los orígenes
# PySide6 NO se ve afectado por CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Authorization", "Content-Type"],
)

# Routers
app.include_router(auth_router)
app.include_router(records_router)
app.include_router(users_router)
app.include_router(coverage_px_router)
app.include_router(shipments_px_router)
app.include_router(receiver_router)
app.include_router(address_router)
app.include_router(contact_router)
app.include_router(job_role_router)
app.include_router(organization_router)
app.include_router(title_router)
app.include_router(volante_router)
app.include_router(sepomex_router)

app.middleware('http')(timing_middleware)


@app.get("/")
def root():
    return {
        "message": "OCR Destinatarios API está funcionando correctamente"
    }

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    custom_errors = []
    for error in exc.errors():
        loc = error.get("loc", [])
        field_name = loc[-1] if loc else 'unknown'
        custom_errors.append({
            "message": error.get('msg', 'Error de validacion'),
            'field': str(field_name),
            'type': error.get('type', 'Validation_error'),
        })

    return JSONResponse(status_code=422, content={'errors': custom_errors})