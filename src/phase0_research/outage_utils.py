from datetime import datetime, timedelta


DATETIME_FORMAT = "%Y-%m-%d %H:%M"


def calculate_duration_minutes(incident_date: str, start_time: str, end_time: str) -> int:
    start = datetime.strptime(f"{incident_date} {start_time}", DATETIME_FORMAT)
    end = datetime.strptime(f"{incident_date} {end_time}", DATETIME_FORMAT)
    if end < start:
        end += timedelta(days=1)
    return int((end - start).total_seconds() // 60)


def normalize_outage_record(record: dict[str, str]) -> dict[str, str]:
    normalized = dict(record)
    normalized["planned_or_unplanned"] = normalized.get("planned_or_unplanned", "unknown").strip().lower()
    normalized["impact_area"] = normalized.get("impact_area", "unknown").strip().lower() or "unknown"

    duration = normalized.get("duration_minutes", "").strip()
    if not duration and normalized.get("incident_date") and normalized.get("start_time") and normalized.get("end_time"):
        normalized["duration_minutes"] = str(
            calculate_duration_minutes(
                normalized["incident_date"],
                normalized["start_time"],
                normalized["end_time"],
            )
        )

    return normalized
