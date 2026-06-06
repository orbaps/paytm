import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from phase0_research.io import read_excel_records, write_csv_records
from phase0_research.outage_utils import normalize_outage_record
from phase0_research.schema_loader import available_datasets, load_schema, schema_fieldnames
from phase0_research.validation import has_errors, validate_records


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest an Excel sheet into a normalized Phase 0 CSV dataset.")
    parser.add_argument("--dataset", required=True, choices=available_datasets())
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--sheet", default=None, help="Excel sheet name. Defaults to the first sheet.")
    parser.add_argument("--append", action="store_true", help="Append to the output instead of replacing it.")
    args = parser.parse_args()

    records = read_excel_records(args.input, args.sheet)
    if args.dataset == "outages":
        records = [normalize_outage_record(record) for record in records]

    schema = load_schema(args.dataset)
    issues = validate_records(records, schema)
    for issue in issues:
        print(issue.format())

    if has_errors(issues):
        print("Ingestion stopped because schema validation failed.")
        return 1

    count = write_csv_records(records, args.output, schema_fieldnames(schema), append=args.append)
    print(f"Ingested {count} {args.dataset} rows from Excel into {args.output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
