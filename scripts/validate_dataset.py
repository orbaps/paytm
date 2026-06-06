import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from phase0_research.io import read_csv_records
from phase0_research.schema_loader import available_datasets, load_schema
from phase0_research.validation import has_errors, validate_records


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Phase 0 CSV dataset against its schema.")
    parser.add_argument("--dataset", required=True, choices=available_datasets())
    parser.add_argument("--file", required=True, type=Path)
    args = parser.parse_args()

    records = read_csv_records(args.file)
    schema = load_schema(args.dataset)
    issues = validate_records(records, schema)

    if not issues:
        print(f"OK: {args.file} has {len(records)} rows and matches the {args.dataset} schema.")
        return 0

    for issue in issues:
        print(issue.format())

    if has_errors(issues):
        print(f"FAILED: {args.file} has schema errors.")
        return 1

    print(f"OK WITH WARNINGS: {args.file} has {len(records)} rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
