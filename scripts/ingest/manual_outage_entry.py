import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from phase0_research.io import write_csv_records
from phase0_research.outage_utils import normalize_outage_record
from phase0_research.schema_loader import load_schema, schema_fieldnames
from phase0_research.validation import has_errors, validate_records


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a manually observed outage to a Phase 0 outage CSV.")
    parser.add_argument("--bank-name", required=True)
    parser.add_argument("--incident-date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--start-time", required=True, help="HH:MM")
    parser.add_argument("--end-time", required=True, help="HH:MM")
    parser.add_argument("--duration-minutes", default="")
    parser.add_argument("--planned-or-unplanned", required=True, choices=["planned", "unplanned", "unknown"])
    parser.add_argument("--source", required=True)
    parser.add_argument("--impact-area", default="unknown")
    parser.add_argument("--notes", default="")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    record = normalize_outage_record(
        {
            "bank_name": args.bank_name,
            "incident_date": args.incident_date,
            "start_time": args.start_time,
            "end_time": args.end_time,
            "duration_minutes": args.duration_minutes,
            "planned_or_unplanned": args.planned_or_unplanned,
            "source": args.source,
            "impact_area": args.impact_area,
            "notes": args.notes,
        }
    )

    schema = load_schema("outages")
    issues = validate_records([record], schema)
    for issue in issues:
        print(issue.format())

    if has_errors(issues):
        print("Manual outage entry was not saved because schema validation failed.")
        return 1

    write_csv_records([record], args.output, schema_fieldnames(schema), append=True)
    print(f"Appended outage for {args.bank_name} on {args.incident_date} to {args.output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
