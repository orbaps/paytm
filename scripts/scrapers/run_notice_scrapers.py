import csv
from pathlib import Path

from bank_notice_scraper import collect_placeholder_notices


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "bank_notices" / "placeholder_notice_targets.csv"
FIELDNAMES = [
    "bank_name",
    "announcement_date",
    "maintenance_start",
    "maintenance_end",
    "description",
    "source_url",
    "notice_status",
]


def main() -> int:
    rows = collect_placeholder_notices()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} placeholder notice targets to {OUTPUT_PATH}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
