from app.core.db import Base
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column

class CoveragePX(Base):
    __tablename__ = "coverages_px"

    id_delivery: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    branch: Mapped[str | None] = mapped_column(String(50)) # Sucursal
    place: Mapped[str | None] = mapped_column(String(30)) # Plaza
    postal_code: Mapped[str] = mapped_column(String(6), nullable=False, index=True)
    colony: Mapped[str] = mapped_column(String(100), nullable=False)
    municipality: Mapped[str] = mapped_column(String(150), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)

    coverage_type: Mapped[Enum] = mapped_column(Enum("PAQUETEXPRESS", "ZONA PLUS", "ZONA PLUS ESPECIAL", name="coverage_type_enum"), nullable=False)

    def __repr__(self) -> str:
        return (f"id_delivery: {self.id_delivery}, branch: {self.branch} place: {self.place}, postal_code: {self.postal_code},\n"
                f"colony: {self.colony}, municipality: {self.municipality},\n"
                f"city: {self.city}, state: {self.state}, coverage_type: {self.coverage_type}")