import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from phase0_research.analysis import downtime_ranking
from phase0_research.io import read_csv_records, write_csv_records


FIELDNAMES = [
    "rank",
    "bank_name",
    "incident_count",
    "total_downtime_minutes",
    "average_duration_minutes",
    "planned_count",
    "unplanned_count",
    "unknown_count",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank banks by total observed downtime.")
    parser.add_argument("--outages", type=Path, default=PROJECT_ROOT / "data" / "samples" / "outages.csv")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "outputs" / "analysis" / "downtime_ranking.csv")
    args = parser.parse_args()

    rows = downtime_ranking(read_csv_records(args.outages))
    write_csv_records(rows, args.output, FIELDNAMES)
    print(f"Wrote downtime ranking for {len(rows)} banks to {args.output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
