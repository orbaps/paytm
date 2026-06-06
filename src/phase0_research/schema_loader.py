import json
from pathlib import Path
from typing import Any

from .paths import SCHEMAS_DIR


SCHEMA_FILES = {
    "banks": "banks.schema.json",
    "outages": "outages.schema.json",
    "maintenance_notices": "maintenance_notices.schema.json",
    "npci_stats": "npci_stats.schema.json",
}


def available_datasets() -> list[str]:
    return sorted(SCHEMA_FILES)


def schema_path(dataset: str) -> Path:
    try:
        return SCHEMAS_DIR / SCHEMA_FILES[dataset]
    except KeyError as exc:
        options = ", ".join(available_datasets())
        raise ValueError(f"Unknown dataset '{dataset}'. Expected one of: {options}") from exc


def load_schema(dataset: str) -> dict[str, Any]:
    path = schema_path(dataset)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def schema_fieldnames(schema: dict[str, Any]) -> list[str]:
    return list(schema.get("columns", {}).keys())
