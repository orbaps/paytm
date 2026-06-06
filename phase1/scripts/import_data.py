import argparse
import sys
from pathlib import Path


PHASE1_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PHASE1_ROOT / "backend"))

from app.db.init_db import init_db
from app.db.session import SessionLocal, engine
from app.services.bulk_import import DATASET_CONFIG, import_upload


def main() -> int:
    parser = argparse.ArgumentParser(description="Import CSV, Excel, or JSON records into the Phase 1 database.")
    parser.add_argument("--dataset", required=True, choices=sorted(DATASET_CONFIG))
    parser.add_argument("--file", required=True, type=Path)
    args = parser.parse_args()

    init_db(engine)
    db = SessionLocal()
    try:
        result = import_upload(db, args.dataset, args.file.name, args.file.read_bytes())
    finally:
        db.close()

    print(result.model_dump_json(indent=2))
    return 1 if result.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
