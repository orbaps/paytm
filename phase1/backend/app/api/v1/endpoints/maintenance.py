from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import MaintenanceNotice
from app.repositories.crud import create_record, delete_record, get_record, list_records, update_record
from app.schemas.common import DeleteResponse
from app.schemas.maintenance_notice import (
    MaintenanceNoticeCreate,
    MaintenanceNoticeRead,
    MaintenanceNoticeUpdate,
)


router = APIRouter()


@router.get("", response_model=list[MaintenanceNoticeRead])
def list_maintenance_notices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_records(db, MaintenanceNotice, skip, limit)


@router.post("", response_model=MaintenanceNoticeRead, status_code=status.HTTP_201_CREATED)
def create_maintenance_notice(payload: MaintenanceNoticeCreate, db: Session = Depends(get_db)):
    return create_record(db, MaintenanceNotice, payload.model_dump())


@router.get("/{notice_id}", response_model=MaintenanceNoticeRead)
def get_maintenance_notice(notice_id: int, db: Session = Depends(get_db)):
    return get_record(db, MaintenanceNotice, notice_id)


@router.put("/{notice_id}", response_model=MaintenanceNoticeRead)
def update_maintenance_notice(notice_id: int, payload: MaintenanceNoticeUpdate, db: Session = Depends(get_db)):
    return update_record(db, MaintenanceNotice, notice_id, payload.model_dump(exclude_unset=True))


@router.delete("/{notice_id}", response_model=DeleteResponse)
def delete_maintenance_notice(notice_id: int, db: Session = Depends(get_db)):
    delete_record(db, MaintenanceNotice, notice_id)
    return DeleteResponse(deleted=True, id=notice_id)
