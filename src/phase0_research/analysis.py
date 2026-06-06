from collections import Counter, defaultdict
from datetime import datetime
from statistics import mean, median
from typing import Iterable


def downtime_ranking(records: Iterable[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, object]] = defaultdict(_bank_summary)

    for record in records:
        bank = record["bank_name"]
        duration = _duration(record)
        summary = grouped[bank]
        summary["bank_name"] = bank
        summary["incident_count"] += 1
        summary["total_downtime_minutes"] += duration
        summary["durations"].append(duration)

        status = record.get("planned_or_unplanned", "unknown")
        if status == "planned":
            summary["planned_count"] += 1
        elif status == "unplanned":
            summary["unplanned_count"] += 1
        else:
            summary["unknown_count"] += 1

    rows = []
    for summary in grouped.values():
        durations = summary.pop("durations")
        summary["average_duration_minutes"] = round(mean(durations), 2) if durations else 0
        rows.append(summary)

    rows.sort(key=lambda row: (-row["total_downtime_minutes"], -row["incident_count"], row["bank_name"]))
    for rank, row in enumerate(rows, start=1):
        row["rank"] = rank
    return rows


def outage_frequency(records: Iterable[dict[str, str]]) -> dict[str, list[dict[str, object]]]:
    bank_counter: Counter[str] = Counter()
    month_counter: Counter[str] = Counter()
    status_by_bank: dict[str, Counter[str]] = defaultdict(Counter)

    for record in records:
        bank = record["bank_name"]
        month = record["incident_date"][:7]
        status = record.get("planned_or_unplanned", "unknown")

        bank_counter[bank] += 1
        month_counter[month] += 1
        status_by_bank[bank][status] += 1

    by_bank = [
        {
            "bank_name": bank,
            "incident_count": count,
            "planned_count": status_by_bank[bank]["planned"],
            "unplanned_count": status_by_bank[bank]["unplanned"],
            "unknown_count": status_by_bank[bank]["unknown"],
        }
        for bank, count in bank_counter.most_common()
    ]

    by_month = [
        {"incident_month": month, "incident_count": count}
        for month, count in sorted(month_counter.items())
    ]

    return {"by_bank": by_bank, "by_month": by_month}


def outage_duration(records: Iterable[dict[str, str]]) -> dict[str, list[dict[str, object]]]:
    durations_by_bank: dict[str, list[int]] = defaultdict(list)
    all_durations: list[int] = []
    longest: dict[str, object] | None = None

    for record in records:
        duration = _duration(record)
        bank = record["bank_name"]
        durations_by_bank[bank].append(duration)
        all_durations.append(duration)
        if longest is None or duration > longest["duration_minutes"]:
            longest = {
                "bank_name": bank,
                "incident_date": record["incident_date"],
                "start_time": record["start_time"],
                "end_time": record["end_time"],
                "duration_minutes": duration,
            }

    by_bank = []
    for bank, durations in durations_by_bank.items():
        by_bank.append(
            {
                "bank_name": bank,
                "incident_count": len(durations),
                "average_duration_minutes": round(mean(durations), 2),
                "median_duration_minutes": round(median(durations), 2),
                "longest_duration_minutes": max(durations),
                "shortest_duration_minutes": min(durations),
            }
        )

    by_bank.sort(key=lambda row: (-row["average_duration_minutes"], row["bank_name"]))

    summary = [
        {
            "incident_count": len(all_durations),
            "average_duration_minutes": round(mean(all_durations), 2) if all_durations else 0,
            "median_duration_minutes": round(median(all_durations), 2) if all_durations else 0,
            "longest_duration_minutes": max(all_durations) if all_durations else 0,
            "shortest_duration_minutes": min(all_durations) if all_durations else 0,
            "longest_incident_bank": longest["bank_name"] if longest else "",
            "longest_incident_date": longest["incident_date"] if longest else "",
        }
    ]

    return {"summary": summary, "by_bank": by_bank}


def planned_vs_unplanned(records: Iterable[dict[str, str]]) -> list[dict[str, object]]:
    status_counter: Counter[str] = Counter()
    duration_counter: Counter[str] = Counter()
    total_incidents = 0
    total_duration = 0

    for record in records:
        status = record.get("planned_or_unplanned", "unknown") or "unknown"
        duration = _duration(record)
        status_counter[status] += 1
        duration_counter[status] += duration
        total_incidents += 1
        total_duration += duration

    rows = []
    for status, count in status_counter.most_common():
        rows.append(
            {
                "planned_or_unplanned": status,
                "incident_count": count,
                "incident_percentage": round((count / total_incidents) * 100, 2) if total_incidents else 0,
                "total_duration_minutes": duration_counter[status],
                "duration_percentage": round((duration_counter[status] / total_duration) * 100, 2)
                if total_duration
                else 0,
            }
        )
    return rows


def heatmap_inputs(records: Iterable[dict[str, str]]) -> dict[str, list[dict[str, object]]]:
    by_day: Counter[str] = Counter()
    by_hour: Counter[str] = Counter()
    by_month: Counter[str] = Counter()

    for record in records:
        date_value = datetime.strptime(record["incident_date"], "%Y-%m-%d")
        by_day[date_value.strftime("%A")] += 1
        by_hour[record["start_time"][:2]] += 1
        by_month[record["incident_date"][:7]] += 1

    return {
        "by_day_of_week": [{"day_of_week": key, "incident_count": value} for key, value in by_day.items()],
        "by_start_hour": [{"start_hour": key, "incident_count": value} for key, value in sorted(by_hour.items())],
        "by_month": [{"incident_month": key, "incident_count": value} for key, value in sorted(by_month.items())],
    }


def _bank_summary() -> dict[str, object]:
    return {
        "bank_name": "",
        "incident_count": 0,
        "total_downtime_minutes": 0,
        "planned_count": 0,
        "unplanned_count": 0,
        "unknown_count": 0,
        "durations": [],
    }


def _duration(record: dict[str, str]) -> int:
    return int(record.get("duration_minutes") or 0)
