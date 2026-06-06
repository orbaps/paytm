import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from phase0_research.analysis import outage_duration
from phase0_research.io import read_csv_records, write_csv_records
from phase0_research.paths import ensure_dir


SUMMARY_FIELDNAMES = [
    "incident_count",
    "average_duration_minutes",
    "median_duration_minutes",
    "longest_duration_minutes",
    "shortest_duration_minutes",
    "longest_incident_bank",
    "longest_incident_date",
]
BY_BANK_FIELDNAMES = [
    "bank_name",
    "incident_count",
    "average_duration_minutes",
    "median_duration_minutes",
    "longest_duration_minutes",
    "shortest_duration_minutes",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze outage duration distributions.")
    parser.add_argument("--outages", type=Path, default=PROJECT_ROOT / "data" / "samples" / "outages.csv")
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "outputs" / "analysis")
    args = parser.parse_args()

    ensure_dir(args.output_dir)
    result = outage_duration(read_csv_records(args.outages))
    write_csv_records(result["summary"], args.output_dir / "outage_duration_summary.csv", SUMMARY_FIELDNAMES)
    write_csv_records(result["by_bank"], args.output_dir / "outage_duration_by_bank.csv", BY_BANK_FIELDNAMES)
    print(f"Wrote outage duration files to {args.output_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
