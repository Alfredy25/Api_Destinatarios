from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class VolanteDto(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class VolanteCreate(BaseModel):
    name: str = Field(..., min_length=18, max_length=35, examples=["VCS-26-131000-00167"])

class VolanteUpdate(BaseModel):
    name: str = Field(..., min_length=18, max_length=35, examples=["VCS-26-131000-00167"])

class PaginatedVolantes(BaseModel):
    search: str | None
    page: int
    page_size: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    items: List[VolanteDto] = Field(default_factory=list)

class TotalsVolantes(BaseModel):
    total: int
    total_pages: int
    current_page: int
    offset: int

    model_config = ConfigDict(from_attributes=True)
