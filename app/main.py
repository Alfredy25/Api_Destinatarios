from fastapi import FastAPI

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

# -----------------------------------------------------------------------------
# Endpoint raíz de prueba
# -----------------------------------------------------------------------------
# Sirve para verificar rápidamente que:
# - El servidor está levantado
# - FastAPI responde correctamente
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "OCR Destinatarios API está funcionando correctamente"
    }