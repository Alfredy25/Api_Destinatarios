from fastapi import FastAPI
from app.api import auth, registros
from fastapi.middleware.cors import CORSMiddleware

# -----------------------------------------------------------------------------
# Punto de entrada principal de la aplicación FastAPI
# -----------------------------------------------------------------------------
# Aquí se:
# - Instancia la aplicación
# - Configuran middlewares (más adelante)
# - Registran routers (más adelante)
# -----------------------------------------------------------------------------

app = FastAPI(
    title="OCR Destinatarios API",
    description="Backend REST para el sistema extractor OCR de destinatarios",
    version="0.1.0"
)


# CORS
# -----------------------------------------------------------------------------
# Configuración controlada
# En producción se deben restringir los orígenes
# PySide6 NO se ve afectado por CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Authorization", "Content-Type"],
)


# Routers
# -----------------------------------------------------------------------------
app.include_router(auth.router)
app.include_router(registros.router)

# -----------------------------------------------------------------------------
# Endpoint raíz de prueba
# Sirve para verificar rápidamente que:
    # - El servidor está levantado
    # - FastAPI responde correctamente

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "OCR Destinatarios API está funcionando correctamente"
    }