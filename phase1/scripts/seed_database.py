import sys
from pathlib import Path


PHASE1_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PHASE1_ROOT / "backend"))

from app.db.init_db import init_db
from app.db.session import SessionLocal, engine
from app.services.seed import seed_database


def main() -> int:
    init_db(engine)
    db = SessionLocal()
    try:
        counts = seed_database(db)
    finally:
        db.close()

    print(
        "Seed complete: "
        f"{counts['banks']} banks, "
        f"{counts['outages']} outages, "
        f"{counts['maintenance_notices']} maintenance notices, "
        f"{counts['npci_statistics']} NPCI statistics."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
