from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Bank
from app.repositories.crud import create_record, delete_record, get_record, list_records, update_record
from app.schemas.bank import BankCreate, BankRead, BankUpdate
from app.schemas.common import DeleteResponse


router = APIRouter()


@router.get("", response_model=list[BankRead])
def list_banks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_records(db, Bank, skip, limit)


@router.post("", response_model=BankRead, status_code=status.HTTP_201_CREATED)
def create_bank(payload: BankCreate, db: Session = Depends(get_db)):
    return create_record(db, Bank, payload.model_dump())


@router.get("/{bank_id}", response_model=BankRead)
def get_bank(bank_id: int, db: Session = Depends(get_db)):
    return get_record(db, Bank, bank_id)


@router.put("/{bank_id}", response_model=BankRead)
def update_bank(bank_id: int, payload: BankUpdate, db: Session = Depends(get_db)):
    return update_record(db, Bank, bank_id, payload.model_dump(exclude_unset=True))


@router.delete("/{bank_id}", response_model=DeleteResponse)
def delete_bank(bank_id: int, db: Session = Depends(get_db)):
    delete_record(db, Bank, bank_id)
    return DeleteResponse(deleted=True, id=bank_id)
