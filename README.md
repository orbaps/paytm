# Paytm Smart Reserve AI - Phase 0 Research Workspace

This repository contains the Phase 0 research foundation for Paytm Smart Reserve AI.

Phase 0 is limited to research and validation:

- Define datasets and schemas.
- Ingest CSV, Excel, and manually entered outage observations.
- Track bank maintenance notices through placeholder scraper modules.
- Run descriptive analysis on outage patterns.
- Prepare report templates for research findings.

No product application, Smart Reserve routing logic, AI model, or prediction system is implemented in this phase.

## Repository Structure

```text
.
|-- Docs/
|   `-- Phase0.md
|-- data/
|   |-- processed/
|   |-- raw/
|   |   |-- bank_notices/
|   |   |-- manual/
|   |   `-- npci/
|   `-- samples/
|       |-- banks.csv
|       |-- maintenance_notices.csv
|       |-- npci_stats.csv
|       `-- outages.csv
|-- notebooks/
|   `-- README.md
|-- outputs/
|   |-- analysis/
|   `-- reports/
|-- reports/
|   `-- templates/
|       |-- bank_rankings.md
|       |-- executive_summary.md
|       `-- outage_patterns.md
|-- schemas/
|   |-- banks.schema.json
|   |-- maintenance_notices.schema.json
|   |-- npci_stats.schema.json
|   `-- outages.schema.json
|-- scripts/
|   |-- analysis/
|   |-- ingest/
|   |-- scrapers/
|   `-- validate_dataset.py
|-- src/
|   `-- phase0_research/
`-- requirements.txt
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The CSV ingestion and analysis scripts use the Python standard library. Excel ingestion needs `pandas` and `openpyxl`.

## Typical Phase 0 Commands

Validate a sample dataset:

```powershell
python scripts/validate_dataset.py --dataset outages --file data/samples/outages.csv
```

Ingest a CSV into the processed research dataset:

```powershell
python scripts/ingest/ingest_csv.py --dataset outages --input data/samples/outages.csv --output data/processed/outages.csv
```

Enter an outage manually:

```powershell
python scripts/ingest/manual_outage_entry.py --bank-name "HDFC Bank" --incident-date 2026-02-14 --start-time 22:15 --end-time 23:05 --planned-or-unplanned unplanned --source "ops desk note" --output data/processed/outages.csv
```

Run all descriptive outage analyses:

```powershell
python scripts/analysis/run_all.py --outages data/samples/outages.csv --output-dir outputs/analysis
```

Check placeholder bank-notice scraper coverage:

```powershell
python scripts/scrapers/run_notice_scrapers.py
```

## Phase Boundary

This workspace intentionally stops at descriptive research outputs. Future phases can consume the normalized datasets and analysis outputs, but should add Smart Reserve product logic, model training, and application code outside Phase 0.
