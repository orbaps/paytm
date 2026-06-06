import csv
import re
from pathlib import Path
from typing import Any, Iterable

from .paths import ensure_dir


def normalize_column_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def clean_cell(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def read_csv_records(path: Path | str) -> list[dict[str, str]]:
    path = Path(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        records: list[dict[str, str]] = []
        for row in reader:
            records.append(
                {
                    normalize_column_name(key): clean_cell(value)
                    for key, value in row.items()
                    if key is not None
                }
            )
    return records


def read_excel_records(path: Path | str, sheet_name: str | int | None = None) -> list[dict[str, str]]:
    try:
        import pandas as pd
    except ImportError as exc:
        raise RuntimeError("Excel ingestion requires pandas and openpyxl. Run: pip install -r requirements.txt") from exc

    sheet = 0 if sheet_name is None else sheet_name
    frame = pd.read_excel(path, sheet_name=sheet, dtype=str)
    frame = frame.fillna("")

    records: list[dict[str, str]] = []
    for raw_record in frame.to_dict(orient="records"):
        records.append(
            {
                normalize_column_name(str(key)): clean_cell(value)
                for key, value in raw_record.items()
            }
        )
    return records


def write_csv_records(
    records: Iterable[dict[str, Any]],
    path: Path | str,
    fieldnames: list[str],
    append: bool = False,
) -> int:
    path = Path(path)
    ensure_dir(path.parent)
    file_exists = path.exists() and path.stat().st_size > 0
    mode = "a" if append else "w"
    count = 0

    with path.open(mode, encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        if not append or not file_exists:
            writer.writeheader()

        for record in records:
            writer.writerow({field: record.get(field, "") for field in fieldnames})
            count += 1

    return count
