import argparse
import sys
from datetime import datetime
from pathlib import Path


PHASE1_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PHASE1_ROOT / "backend"))

from app.db.init_db import init_db
from app.db.session import SessionLocal, engine
from app.models import Outage
from app.repositories.crud import create_record
from app.schemas.outage import OutageCreate


def main() -> int:
    parser = argparse.ArgumentParser(description="Create one manually observed outage record.")
    parser.add_argument("--bank-id", required=True, type=int)
    parser.add_argument("--outage-type", required=True)
    parser.add_argument("--planned", action="store_true")
    parser.add_argument("--severity", required=True, choices=["low", "medium", "high", "critical"])
    parser.add_argument("--start-time", required=True, help="ISO timestamp, for example 2026-01-05T10:00:00+05:30")
    parser.add_argument("--end-time", required=True, help="ISO timestamp, for example 2026-01-05T10:45:00+05:30")
    parser.add_argument("--source", required=True)
    args = parser.parse_args()

    payload = OutageCreate(
        bank_id=args.bank_id,
        outage_type=args.outage_type,
        planned=args.planned,
        severity=args.severity,
        start_time=datetime.fromisoformat(args.start_time),
        end_time=datetime.fromisoformat(args.end_time),
        source=args.source,
    )

    init_db(engine)
    db = SessionLocal()
    try:
        outage = create_record(db, Outage, payload.model_dump())
    finally:
        db.close()

    print(f"Created outage id={outage.id} duration_minutes={outage.duration_minutes}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
