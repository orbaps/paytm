import csv
import io
import json
import re
from pathlib import Path
from typing import Any


def normalize_column_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    return {normalize_column_name(str(key)): value for key, value in record.items()}


def read_records_from_upload(filename: str, content: bytes) -> list[dict[str, Any]]:
    suffix = Path(filename).suffix.lower()
    if suffix == ".csv":
        return _read_csv(content)
    if suffix == ".json":
        return _read_json(content)
    if suffix in {".xlsx", ".xls"}:
        return _read_excel(content, suffix)
    raise ValueError("Unsupported file type. Use CSV, JSON, XLSX, or XLS.")


def read_records_from_path(path: Path) -> list[dict[str, Any]]:
    content = path.read_bytes()
    return read_records_from_upload(path.name, content)


def _read_csv(content: bytes) -> list[dict[str, Any]]:
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    return [normalize_record(row) for row in reader]


def _read_json(content: bytes) -> list[dict[str, Any]]:
    payload = json.loads(content.decode("utf-8"))
    if isinstance(payload, dict):
        if "records" in payload:
            payload = payload["records"]
        else:
            values = [value for value in payload.values() if isinstance(value, list)]
            payload = values[0] if values else []
    if not isinstance(payload, list):
        raise ValueError("JSON import must contain a list of records.")
    return [normalize_record(record) for record in payload]


def _read_excel(content: bytes, suffix: str) -> list[dict[str, Any]]:
    try:
        import pandas as pd
    except ImportError as exc:
        raise RuntimeError("Excel import requires pandas and openpyxl.") from exc

    frame = pd.read_excel(io.BytesIO(content), dtype=str)
    frame = frame.fillna("")
    return [normalize_record(record) for record in frame.to_dict(orient="records")]
