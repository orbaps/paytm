import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from phase0_research.analysis import outage_frequency
from phase0_research.io import read_csv_records, write_csv_records
from phase0_research.paths import ensure_dir


BANK_FIELDNAMES = ["bank_name", "incident_count", "planned_count", "unplanned_count", "unknown_count"]
MONTH_FIELDNAMES = ["incident_month", "incident_count"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze outage frequency by bank and month.")
    parser.add_argument("--outages", type=Path, default=PROJECT_ROOT / "data" / "samples" / "outages.csv")
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "outputs" / "analysis")
    args = parser.parse_args()

    ensure_dir(args.output_dir)
    result = outage_frequency(read_csv_records(args.outages))
    bank_output = args.output_dir / "outage_frequency_by_bank.csv"
    month_output = args.output_dir / "outage_frequency_by_month.csv"

    write_csv_records(result["by_bank"], bank_output, BANK_FIELDNAMES)
    write_csv_records(result["by_month"], month_output, MONTH_FIELDNAMES)
    print(f"Wrote outage frequency files to {args.output_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
