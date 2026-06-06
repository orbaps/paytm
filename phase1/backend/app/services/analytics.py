from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.models import Bank, MaintenanceNotice, NPCIStatistic, Outage
from app.schemas.dashboard import (
    AverageDowntime,
    DashboardSummary,
    DashboardTrends,
    MonthlyCount,
    NamedCount,
    PlannedSplit,
)


def get_dashboard_summary(db: Session) -> DashboardSummary:
    outage_count = db.query(func.count(Outage.id)).scalar() or 0
    planned_count = db.query(func.count(Outage.id)).filter(Outage.planned.is_(True)).scalar() or 0

    return DashboardSummary(
        bank_count=db.query(func.count(Bank.id)).scalar() or 0,
        outage_count=outage_count,
        planned_outage_count=planned_count,
        unplanned_outage_count=outage_count - planned_count,
        maintenance_notice_count=db.query(func.count(MaintenanceNotice.id)).scalar() or 0,
        npci_statistic_count=db.query(func.count(NPCIStatistic.id)).scalar() or 0,
    )


def get_dashboard_trends(db: Session) -> DashboardTrends:
    outage_year = extract("year", Outage.start_time)
    outage_month = extract("month", Outage.start_time)

    outages_by_bank = [
        NamedCount(name=bank_name, count=count)
        for bank_name, count in (
            db.query(Bank.bank_name, func.count(Outage.id))
            .join(Outage, Outage.bank_id == Bank.id)
            .group_by(Bank.bank_name)
            .order_by(func.count(Outage.id).desc())
            .limit(12)
            .all()
        )
    ]

    outages_by_month = [
        MonthlyCount(month=f"{int(year):04d}-{int(month):02d}", count=count)
        for year, month, count in (
            db.query(
                outage_year.label("year"),
                outage_month.label("month"),
                func.count(Outage.id),
            )
            .group_by(outage_year, outage_month)
            .order_by(outage_year, outage_month)
            .all()
        )
    ]

    average_downtime = [
        AverageDowntime(bank_name=bank_name, average_duration_minutes=round(float(avg_duration or 0), 2))
        for bank_name, avg_duration in (
            db.query(Bank.bank_name, func.avg(Outage.duration_minutes))
            .join(Outage, Outage.bank_id == Bank.id)
            .group_by(Bank.bank_name)
            .order_by(func.avg(Outage.duration_minutes).desc())
            .limit(12)
            .all()
        )
    ]

    planned = db.query(func.count(Outage.id)).filter(Outage.planned.is_(True)).scalar() or 0
    unplanned = db.query(func.count(Outage.id)).filter(Outage.planned.is_(False)).scalar() or 0

    return DashboardTrends(
        outages_by_bank=outages_by_bank,
        outages_by_month=outages_by_month,
        average_downtime_by_bank=average_downtime,
        planned_vs_unplanned=[
            PlannedSplit(label="planned", count=planned),
            PlannedSplit(label="unplanned", count=unplanned),
        ],
    )
