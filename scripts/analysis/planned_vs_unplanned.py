import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from phase0_research.analysis import planned_vs_unplanned
from phase0_research.io import read_csv_records, write_csv_records


FIELDNAMES = [
    "planned_or_unplanned",
    "incident_count",
    "incident_percentage",
    "total_duration_minutes",
    "duration_percentage",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare planned and unplanned outage patterns.")
    parser.add_argument("--outages", type=Path, default=PROJECT_ROOT / "data" / "samples" / "outages.csv")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "outputs" / "analysis" / "planned_vs_unplanned.csv")
    args = parser.parse_args()

    rows = planned_vs_unplanned(read_csv_records(args.outages))
    write_csv_records(rows, args.output, FIELDNAMES)
    print(f"Wrote planned-vs-unplanned analysis to {args.output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
