from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.imports import ImportResult
from app.services.bulk_import import DATASET_CONFIG, import_upload


router = APIRouter()


@router.post("/{dataset}", response_model=ImportResult)
async def import_dataset(dataset: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if dataset not in DATASET_CONFIG:
        allowed = ", ".join(sorted(DATASET_CONFIG))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown dataset '{dataset}'. Expected one of: {allowed}",
        )
    return import_upload(db, dataset, file.filename or "upload.csv", await file.read())
