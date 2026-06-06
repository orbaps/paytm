from typing import Any, TypeVar

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.base import Base


ModelT = TypeVar("ModelT", bound=Base)


def list_records(db: Session, model: type[ModelT], skip: int = 0, limit: int = 100) -> list[ModelT]:
    return list(db.query(model).offset(skip).limit(limit).all())


def get_record(db: Session, model: type[ModelT], record_id: int) -> ModelT:
    record = db.get(model, record_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model.__name__} not found")
    return record


def create_record(db: Session, model: type[ModelT], payload: dict[str, Any]) -> ModelT:
    record = model(**payload)
    db.add(record)
    return _commit(db, record)


def update_record(db: Session, model: type[ModelT], record_id: int, payload: dict[str, Any]) -> ModelT:
    record = get_record(db, model, record_id)
    for key, value in payload.items():
        if value is not None:
            setattr(record, key, value)
    return _commit(db, record)


def delete_record(db: Session, model: type[ModelT], record_id: int) -> None:
    record = get_record(db, model, record_id)
    db.delete(record)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Database constraint violation",
        ) from exc


def _commit(db: Session, record: ModelT) -> ModelT:
    try:
        db.commit()
        db.refresh(record)
        return record
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Database constraint violation",
        ) from exc
