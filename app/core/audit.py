from enum import Enum
from typing import Any

from sqlalchemy.orm import Session

from app.entities.audit_log import AuditLog

TITLE_FIELDS = ("abbreviation", "meaning")
VOLANTE_FIELDS = ("name",)
JOB_FIELDS = ("abbreviation", "meaning")
ORGANIZATION_FIELDS = ("name", "state")
ADDRESS_FIELDS = (
    "street",
    "num_street",
    "colony",
    "municipality",
    "city",
    "state",
    "postal_code",
    "country",
    "address_reference",
)
CONTACT_FIELDS = ("phone", "ext")


def stamp_new(entity: Any, user_id: int) -> None:
    """Marca quién creó la fila. No se usa sobre registros que ya existían."""
    entity.created_by = user_id
    entity.updated_by = user_id


def jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    return value


def snapshot(entity: Any, fields: tuple[str, ...]) -> dict[str, Any]:
    return {field: jsonable(getattr(entity, field)) for field in fields}


def diff_updates(entity: Any, updates: dict, tracked: tuple[str, ...]) -> dict:
    """Compara el valor guardado con el que se va a escribir."""
    changes: dict[str, dict[str, Any]] = {}
    tracked_fields = set(tracked)
    for field, new_value in updates.items():
        if field not in tracked_fields:
            continue
        old_value = jsonable(getattr(entity, field))
        stored_value = jsonable(new_value)
        if old_value != stored_value:
            changes[field] = {"old": old_value, "new": stored_value}
    return changes


def diff_snapshots(before: dict, after: dict) -> dict:
    changes: dict[str, dict[str, Any]] = {}
    for field, old_value in before.items():
        new_value = after.get(field)
        if old_value != new_value:
            changes[field] = {"old": old_value, "new": new_value}
    return changes


def record_update(db: Session, entity: Any, user_id: int, changes: dict) -> None:
    """Guarda el historial y el último editor solo si algún campo cambió."""
    if not changes:
        return
    entity.updated_by = user_id
    db.add(
        AuditLog(
            entity_name=entity.__tablename__,
            entity_id=entity.id,
            user_id=user_id,
            changes=changes,
        )
    )
