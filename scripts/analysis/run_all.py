import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from phase0_research.analysis import (
    downtime_ranking,
    heatmap_inputs,
    outage_duration,
    outage_frequency,
    planned_vs_unplanned,
)
from phase0_research.io import read_csv_records, write_csv_records
from phase0_research.paths import ensure_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Run all Phase 0 outage analysis scripts.")
    parser.add_argument("--outages", type=Path, default=PROJECT_ROOT / "data" / "samples" / "outages.csv")
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "outputs" / "analysis")
    args = parser.parse_args()

    ensure_dir(args.output_dir)
    records = read_csv_records(args.outages)

    write_csv_records(
        downtime_ranking(records),
        args.output_dir / "downtime_ranking.csv",
        [
            "rank",
            "bank_name",
            "incident_count",
            "total_downtime_minutes",
            "average_duration_minutes",
            "planned_count",
            "unplanned_count",
            "unknown_count",
        ],
    )

    frequency = outage_frequency(records)
    write_csv_records(
        frequency["by_bank"],
        args.output_dir / "outage_frequency_by_bank.csv",
        ["bank_name", "incident_count", "planned_count", "unplanned_count", "unknown_count"],
    )
    write_csv_records(
        frequency["by_month"],
        args.output_dir / "outage_frequency_by_month.csv",
        ["incident_month", "incident_count"],
    )

    duration = outage_duration(records)
    write_csv_records(
        duration["summary"],
        args.output_dir / "outage_duration_summary.csv",
        [
            "incident_count",
            "average_duration_minutes",
            "median_duration_minutes",
            "longest_duration_minutes",
            "shortest_duration_minutes",
            "longest_incident_bank",
            "longest_incident_date",
        ],
    )
    write_csv_records(
        duration["by_bank"],
        args.output_dir / "outage_duration_by_bank.csv",
        [
            "bank_name",
            "incident_count",
            "average_duration_minutes",
            "median_duration_minutes",
            "longest_duration_minutes",
            "shortest_duration_minutes",
        ],
    )

    write_csv_records(
        planned_vs_unplanned(records),
        args.output_dir / "planned_vs_unplanned.csv",
        [
            "planned_or_unplanned",
            "incident_count",
            "incident_percentage",
            "total_duration_minutes",
            "duration_percentage",
        ],
    )

    heatmap = heatmap_inputs(records)
    write_csv_records(heatmap["by_day_of_week"], args.output_dir / "heatmap_by_day_of_week.csv", ["day_of_week", "incident_count"])
    write_csv_records(heatmap["by_start_hour"], args.output_dir / "heatmap_by_start_hour.csv", ["start_hour", "incident_count"])
    write_csv_records(heatmap["by_month"], args.output_dir / "heatmap_by_month.csv", ["incident_month", "incident_count"])

    print(f"Wrote all Phase 0 analysis outputs to {args.output_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
