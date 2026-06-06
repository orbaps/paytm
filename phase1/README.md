# Paytm Smart Reserve AI - Phase 1 Data Collection Platform

Phase 1 implements the centralized outage intelligence data platform that later Smart Reserve phases can consume.

This phase includes:

- FastAPI backend.
- SQLAlchemy models.
- PostgreSQL schema.
- CRUD APIs for banks, outages, maintenance notices, and NPCI statistics.
- CSV, Excel, and JSON import utilities.
- Realistic seed-data generation.
- React and Tailwind admin dashboard.
- Docker support.
- Environment configuration.
- Request logging, basic authentication, rate limiting, and unit tests.

This phase does not include Smart Reserve logic, risk scoring, machine learning, prediction models, or notifications.

## Structure

```text
phase1/
|-- backend/
|   |-- app/
|   |-- tests/
|   |-- Dockerfile
|   |-- pytest.ini
|   `-- requirements.txt
|-- database/
|   `-- schema.sql
|-- docs/
|-- frontend/
|   |-- src/
|   |-- Dockerfile
|   `-- package.json
|-- scripts/
|   |-- import_data.py
|   |-- manual_outage_entry.py
|   `-- seed_database.py
|-- tests/
|-- .env.example
`-- docker-compose.yml
```

## Run With Docker

```powershell
cd phase1
docker compose up --build
```

Optional local overrides:

```powershell
Copy-Item .env.example .env
```

Services:

- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Frontend dashboard: `http://localhost:5173`
- PostgreSQL: `localhost:5432`

Default API credentials:

- Username: `admin`
- Password: `admin123`

## Seed Data

After the backend and database are running:

```powershell
cd phase1
docker compose exec backend python -m app.cli.seed_database
```

For local backend development, `python scripts/seed_database.py` is also available.

The seed utility creates:

- 8 banks
- 100 outage records
- 50 maintenance notices
- 12 months of NPCI statistics for each bank

## API Examples

```powershell
curl -u admin:admin123 http://localhost:8000/api/banks
curl -u admin:admin123 http://localhost:8000/api/outages
curl -u admin:admin123 http://localhost:8000/api/maintenance
curl -u admin:admin123 http://localhost:8000/api/statistics
curl -u admin:admin123 http://localhost:8000/api/dashboard/summary
```

Upload CSV, Excel, or JSON:

```powershell
curl -u admin:admin123 -F "file=@banks.csv" http://localhost:8000/api/imports/banks
curl -u admin:admin123 -F "file=@npci.csv" http://localhost:8000/api/statistics/upload
```

Supported import datasets:

- `banks`
- `outages`
- `maintenance_notices`
- `npci_statistics`

## Local Backend Development

```powershell
cd phase1/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Local Frontend Development

```powershell
cd phase1/frontend
npm install
npm run dev
```

## Tests

```powershell
cd phase1/backend
pytest
```

Tests use an in-memory SQLite database for fast API-level checks. PostgreSQL remains the production database target for Phase 1.
