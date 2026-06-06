from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import NPCIStatistic
from app.repositories.crud import create_record, delete_record, get_record, list_records, update_record
from app.schemas.common import DeleteResponse
from app.schemas.imports import ImportResult
from app.schemas.npci_statistic import NPCIStatisticCreate, NPCIStatisticRead, NPCIStatisticUpdate
from app.services.bulk_import import import_upload


router = APIRouter()


@router.get("", response_model=list[NPCIStatisticRead])
def list_statistics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_records(db, NPCIStatistic, skip, limit)


@router.post("", response_model=NPCIStatisticRead, status_code=status.HTTP_201_CREATED)
def create_statistic(payload: NPCIStatisticCreate, db: Session = Depends(get_db)):
    return create_record(db, NPCIStatistic, payload.model_dump())


@router.post("/upload", response_model=ImportResult)
async def upload_statistics(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return import_upload(db, "npci_statistics", file.filename or "upload.csv", await file.read())


@router.get("/{statistic_id}", response_model=NPCIStatisticRead)
def get_statistic(statistic_id: int, db: Session = Depends(get_db)):
    return get_record(db, NPCIStatistic, statistic_id)


@router.put("/{statistic_id}", response_model=NPCIStatisticRead)
def update_statistic(statistic_id: int, payload: NPCIStatisticUpdate, db: Session = Depends(get_db)):
    return update_record(db, NPCIStatistic, statistic_id, payload.model_dump(exclude_unset=True))


@router.delete("/{statistic_id}", response_model=DeleteResponse)
def delete_statistic(statistic_id: int, db: Session = Depends(get_db)):
    delete_record(db, NPCIStatistic, statistic_id)
    return DeleteResponse(deleted=True, id=statistic_id)
