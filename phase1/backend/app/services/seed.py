from datetime import datetime, timedelta, timezone
from decimal import Decimal
from random import Random

from sqlalchemy.orm import Session

from app.models import Bank, MaintenanceNotice, NPCIStatistic, Outage


BANKS = [
    ("State Bank of India", "public_sector", True),
    ("HDFC Bank", "private_sector", True),
    ("ICICI Bank", "private_sector", True),
    ("Axis Bank", "private_sector", True),
    ("Kotak Mahindra Bank", "private_sector", True),
    ("Punjab National Bank", "public_sector", True),
    ("Bank of Baroda", "public_sector", True),
    ("Canara Bank", "public_sector", True),
]

OUTAGE_TYPES = ["upi", "netbanking", "mobile_banking", "cards", "multiple"]
SEVERITIES = ["low", "medium", "high", "critical"]


def seed_database(db: Session) -> dict[str, int]:
    if db.query(Bank).count() > 0:
        return {"banks": 0, "outages": 0, "maintenance_notices": 0, "npci_statistics": 0}

    rng = Random(42)
    banks = [
        Bank(bank_name=bank_name, bank_type=bank_type, upi_enabled=upi_enabled)
        for bank_name, bank_type, upi_enabled in BANKS
    ]
    db.add_all(banks)
    db.flush()

    outage_rows = _build_outages(rng, banks)
    notice_rows = _build_maintenance_notices(rng, banks)
    statistic_rows = _build_npci_statistics(rng, banks)

    db.add_all(outage_rows + notice_rows + statistic_rows)
    db.commit()

    return {
        "banks": len(banks),
        "outages": len(outage_rows),
        "maintenance_notices": len(notice_rows),
        "npci_statistics": len(statistic_rows),
    }


def _build_outages(rng: Random, banks: list[Bank]) -> list[Outage]:
    rows: list[Outage] = []
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)

    for index in range(100):
        bank = banks[index % len(banks)]
        planned = index % 3 == 0
        start = base + timedelta(days=rng.randint(0, 179), hours=rng.choice([0, 1, 2, 9, 13, 18, 21, 23]))
        duration = rng.choice([20, 30, 45, 60, 75, 90, 120, 150])
        severity = rng.choices(SEVERITIES, weights=[20, 45, 25, 10], k=1)[0]
        rows.append(
            Outage(
                bank_id=bank.id,
                outage_type=rng.choice(OUTAGE_TYPES),
                planned=planned,
                severity=severity,
                start_time=start,
                end_time=start + timedelta(minutes=duration),
                duration_minutes=duration,
                source="seed data: bank notice" if planned else "seed data: ops desk observation",
            )
        )
    return rows


def _build_maintenance_notices(rng: Random, banks: list[Bank]) -> list[MaintenanceNotice]:
    rows: list[MaintenanceNotice] = []
    base = datetime(2026, 1, 5, tzinfo=timezone.utc)

    for index in range(50):
        bank = banks[index % len(banks)]
        start = base + timedelta(days=index * 3, hours=rng.choice([0, 1, 2, 23]))
        duration = rng.choice([60, 90, 120])
        rows.append(
            MaintenanceNotice(
                bank_id=bank.id,
                title=f"{bank.bank_name} scheduled digital banking maintenance",
                description="Scheduled maintenance for UPI, mobile banking, or internet banking channels.",
                maintenance_start=start,
                maintenance_end=start + timedelta(minutes=duration),
                source="seed data: maintenance notice",
            )
        )
    return rows


def _build_npci_statistics(rng: Random, banks: list[Bank]) -> list[NPCIStatistic]:
    rows: list[NPCIStatistic] = []

    for bank in banks:
        base_success = Decimal(str(round(rng.uniform(97.2, 98.6), 2)))
        for month in range(1, 13):
            technical_decline = Decimal(str(round(rng.uniform(0.35, 1.15), 2)))
            business_decline = Decimal(str(round(rng.uniform(0.85, 1.9), 2)))
            rows.append(
                NPCIStatistic(
                    bank_id=bank.id,
                    month=month,
                    year=2026,
                    success_rate=max(Decimal("0"), base_success - technical_decline / Decimal("10")),
                    technical_decline=technical_decline,
                    business_decline=business_decline,
                    source="seed data: mock NPCI monthly statistics",
                )
            )
    return rows
