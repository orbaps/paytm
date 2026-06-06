from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Outage
from app.repositories.crud import create_record, delete_record, get_record, list_records, update_record
from app.schemas.common import DeleteResponse
from app.schemas.outage import OutageCreate, OutageRead, OutageUpdate


router = APIRouter()


@router.get("", response_model=list[OutageRead])
def list_outages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_records(db, Outage, skip, limit)


@router.post("", response_model=OutageRead, status_code=status.HTTP_201_CREATED)
def create_outage(payload: OutageCreate, db: Session = Depends(get_db)):
    return create_record(db, Outage, payload.model_dump())


@router.get("/{outage_id}", response_model=OutageRead)
def get_outage(outage_id: int, db: Session = Depends(get_db)):
    return get_record(db, Outage, outage_id)


@router.put("/{outage_id}", response_model=OutageRead)
def update_outage(outage_id: int, payload: OutageUpdate, db: Session = Depends(get_db)):
    return update_record(db, Outage, outage_id, payload.model_dump(exclude_unset=True))


@router.delete("/{outage_id}", response_model=DeleteResponse)
def delete_outage(outage_id: int, db: Session = Depends(get_db)):
    delete_record(db, Outage, outage_id)
    return DeleteResponse(deleted=True, id=outage_id)
