import logging
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

from fastapi import Request

LOGS_DIR = Path(__file__).resolve().parents[2] / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("request_timing")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    formatter = logging.Formatter("%(message)s")

    file_handler = RotatingFileHandler(
        LOGS_DIR / "requests.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


async def timing_middleware(request: Request, call_next):
    request_datetime = datetime.now()
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.6f}s"
    logger.info(
        f"{request_datetime:%Y-%m-%d %H:%M:%S} | "
        f"{request.method} {request.url} -> {response.status_code}: {process_time:.6f}s"
    )
    return response
