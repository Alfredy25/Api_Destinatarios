from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.v1.volante.repository import VolanteRepository
from app.api.v1.volante.schemas import VolanteDto, VolanteCreate, PaginatedVolantes, VolanteUpdate
from app.core.audit import VOLANTE_FIELDS, diff_updates, record_update, stamp_new
from app.entities import VolanteORM
from app.entities.user import User


class VolanteService:
    def __init__(self, db: Session, repo: VolanteRepository):
        self._db = db
        self._repo = repo

    def find_all(self,
                 search: str | None,
                 page: int,
                 page_size: int,
                 order_by: str,
                 direction: str) -> PaginatedVolantes:
        search_find = search.strip().upper() if search else None

        totals, volantes_orm = self._repo.list_all(
            search_find, page, page_size, order_by, direction
        )

        total = totals.total
        total_pages = totals.total_pages
        current_page = totals.current_page

        has_prev = current_page > 1 and total > 0
        has_next = current_page < total_pages if total_pages > 0 else False

        items = [
            VolanteDto.model_validate(volante_orm, from_attributes=True)
            for volante_orm in volantes_orm
        ]
        return PaginatedVolantes(
            search=search_find,
            page=current_page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
            has_prev=has_prev,
            has_next=has_next,
            items=items
        )

    def create_volante(self, volante: VolanteCreate, user: User) -> VolanteDto:
        volante_orm = self._repo.get_by_name(volante.name.upper())
        if volante_orm:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Volante ya existe")

        volante.name = volante.name.strip().upper()
        try:
            volante_orm = self._repo.create(volante.name.upper())
            stamp_new(volante_orm, user.id)
            self._db.commit()
            self._db.refresh(volante_orm)
            return VolanteDto.model_validate(volante_orm, from_attributes=True)
        except SQLAlchemyError as e:
            self._db.rollback()
            raise

    def update_volante(self, volante_id: int, volante: VolanteUpdate, user: User):
        volante_orm = self._repo.find_by_id(volante_id)
        if not volante_orm:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volante no existe")
        updates = volante.model_dump()
        updates["name"] = updates.get("name").strip().upper()
        existing = self._repo.get_by_name(updates.get("name"))
        if existing and existing.id != volante_orm.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="name de volante ya existe")
        try:
            changes = diff_updates(volante_orm, updates, VOLANTE_FIELDS)
            volante_orm = self._repo.update(volante_orm, updates)
            record_update(self._db, volante_orm, user.id, changes)
            self._db.commit()
            self._db.refresh(volante_orm)
            return VolanteDto.model_validate(volante_orm, from_attributes=True)
        except SQLAlchemyError as e:
            self._db.rollback()
            raise

    def ensure_volante(self, volante: VolanteCreate, user: User) -> VolanteORM:
        volante_orm = self._repo.get_by_name(volante.name.upper())
        if volante_orm:
            return volante_orm

        volante_orm_new = self._repo.create(volante.name.upper())
        stamp_new(volante_orm_new, user.id)
        self._db.flush()
        return volante_orm_new






