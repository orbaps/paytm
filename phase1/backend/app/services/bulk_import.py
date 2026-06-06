from typing import Any

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.models import Bank, MaintenanceNotice, NPCIStatistic, Outage
from app.repositories.crud import create_record
from app.schemas.bank import BankCreate
from app.schemas.imports import ImportResult
from app.schemas.maintenance_notice import MaintenanceNoticeCreate
from app.schemas.npci_statistic import NPCIStatisticCreate
from app.schemas.outage import OutageCreate
from app.services.importers import read_records_from_upload


DATASET_CONFIG = {
    "banks": (Bank, BankCreate),
    "outages": (Outage, OutageCreate),
    "maintenance_notices": (MaintenanceNotice, MaintenanceNoticeCreate),
    "npci_statistics": (NPCIStatistic, NPCIStatisticCreate),
}


def import_upload(db: Session, dataset: str, filename: str, content: bytes) -> ImportResult:
    if dataset not in DATASET_CONFIG:
        raise ValueError(f"Unknown dataset '{dataset}'")

    model, schema = DATASET_CONFIG[dataset]
    records = read_records_from_upload(filename, content)
    imported = 0
    errors: list[str] = []

    for index, record in enumerate(records, start=1):
        try:
            payload = schema(**_coerce_record(record)).model_dump()
            create_record(db, model, payload)
            imported += 1
        except (ValidationError, ValueError) as exc:
            errors.append(f"row {index}: {exc}")
        except Exception as exc:  # Keep bulk import moving, but report failures.
            errors.append(f"row {index}: {exc}")

    return ImportResult(dataset=dataset, imported=imported, failed=len(errors), errors=errors)


def _coerce_record(record: dict[str, Any]) -> dict[str, Any]:
    coerced = dict(record)
    for key, value in list(coerced.items()):
        if value == "":
            coerced[key] = None
        elif isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in {"true", "false"}:
                coerced[key] = lowered == "true"
    return coerced
