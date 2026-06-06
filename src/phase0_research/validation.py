from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    message: str
    row_number: int | None = None
    column: str | None = None

    def format(self) -> str:
        location = []
        if self.row_number is not None:
            location.append(f"row {self.row_number}")
        if self.column:
            location.append(self.column)
        prefix = " / ".join(location) if location else "dataset"
        return f"[{self.severity.upper()}] {prefix}: {self.message}"


def validate_records(records: list[dict[str, str]], schema: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    columns = schema.get("columns", {})
    required = set(schema.get("required", []))
    expected = set(columns)

    observed = set()
    for record in records:
        observed.update(record.keys())

    for column in sorted(required - observed):
        issues.append(ValidationIssue("error", "required column is missing", column=column))

    for column in sorted(observed - expected):
        issues.append(ValidationIssue("warning", "column is not defined in schema", column=column))

    for row_index, record in enumerate(records, start=2):
        for column in required:
            if not record.get(column, "").strip():
                issues.append(ValidationIssue("error", "required value is missing", row_index, column))

        for column, value in record.items():
            if column not in columns or value == "":
                continue
            issues.extend(_validate_value(row_index, column, value, columns[column]))

    return issues


def has_errors(issues: list[ValidationIssue]) -> bool:
    return any(issue.severity == "error" for issue in issues)


def _validate_value(
    row_number: int,
    column: str,
    value: str,
    spec: dict[str, Any],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    data_type = spec.get("type", "string")

    try:
        parsed = _parse_value(value, data_type)
    except ValueError as exc:
        return [ValidationIssue("error", str(exc), row_number, column)]

    enum_values = spec.get("enum")
    if enum_values and value not in enum_values:
        allowed = ", ".join(enum_values)
        issues.append(ValidationIssue("error", f"expected one of: {allowed}", row_number, column))

    minimum = spec.get("minimum")
    maximum = spec.get("maximum")
    if minimum is not None and isinstance(parsed, (int, float)) and parsed < minimum:
        issues.append(ValidationIssue("error", f"must be >= {minimum}", row_number, column))
    if maximum is not None and isinstance(parsed, (int, float)) and parsed > maximum:
        issues.append(ValidationIssue("error", f"must be <= {maximum}", row_number, column))

    return issues


def _parse_value(value: str, data_type: str) -> str | int | float | bool:
    if data_type == "string":
        return value
    if data_type == "boolean":
        lowered = value.lower()
        if lowered in {"true", "false", "yes", "no", "1", "0"}:
            return lowered in {"true", "yes", "1"}
        raise ValueError("expected boolean value")
    if data_type == "integer":
        try:
            return int(value)
        except ValueError as exc:
            raise ValueError("expected integer value") from exc
    if data_type == "number":
        try:
            return float(value)
        except ValueError as exc:
            raise ValueError("expected numeric value") from exc
    if data_type == "date":
        _parse_datetime(value, "%Y-%m-%d", "expected date as YYYY-MM-DD")
        return value
    if data_type == "time":
        _parse_datetime(value, "%H:%M", "expected time as HH:MM")
        return value
    if data_type == "datetime":
        _parse_datetime(value, "%Y-%m-%d %H:%M", "expected datetime as YYYY-MM-DD HH:MM")
        return value
    if data_type == "month":
        _parse_datetime(value, "%Y-%m", "expected month as YYYY-MM")
        return value
    raise ValueError(f"unsupported schema type '{data_type}'")


def _parse_datetime(value: str, fmt: str, message: str) -> None:
    try:
        datetime.strptime(value, fmt)
    except ValueError as exc:
        raise ValueError(message) from exc
