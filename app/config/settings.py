import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Settings(BaseModel):
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "secret-jwt-token")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXP_MINUTES: int = int(os.getenv("JWT_EXP_MINUTES", 60))
    DATABASE_URI: str = os.getenv("DATABASE_URI")


settings = Settings()
