# Phase 1 API

All `/api/*` endpoints use HTTP Basic authentication by default.

## Banks

- `GET /api/banks`
- `POST /api/banks`
- `GET /api/banks/{bank_id}`
- `PUT /api/banks/{bank_id}`
- `DELETE /api/banks/{bank_id}`

## Outages

- `GET /api/outages`
- `POST /api/outages`
- `GET /api/outages/{outage_id}`
- `PUT /api/outages/{outage_id}`
- `DELETE /api/outages/{outage_id}`

## Maintenance

- `GET /api/maintenance`
- `POST /api/maintenance`
- `GET /api/maintenance/{notice_id}`
- `PUT /api/maintenance/{notice_id}`
- `DELETE /api/maintenance/{notice_id}`

## NPCI Statistics

- `GET /api/statistics`
- `POST /api/statistics`
- `POST /api/statistics/upload`
- `GET /api/statistics/{statistic_id}`
- `PUT /api/statistics/{statistic_id}`
- `DELETE /api/statistics/{statistic_id}`

## Imports

- `POST /api/imports/{dataset}`

Supported dataset values:

- `banks`
- `outages`
- `maintenance_notices`
- `npci_statistics`

Supported file formats:

- CSV
- JSON
- Excel

## Dashboard

- `GET /api/dashboard/summary`
- `GET /api/dashboard/trends`
