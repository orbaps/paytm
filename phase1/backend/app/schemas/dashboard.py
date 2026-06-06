from pydantic import BaseModel


class DashboardSummary(BaseModel):
    bank_count: int
    outage_count: int
    planned_outage_count: int
    unplanned_outage_count: int
    maintenance_notice_count: int
    npci_statistic_count: int


class NamedCount(BaseModel):
    name: str
    count: int


class MonthlyCount(BaseModel):
    month: str
    count: int


class AverageDowntime(BaseModel):
    bank_name: str
    average_duration_minutes: float


class PlannedSplit(BaseModel):
    label: str
    count: int


class DashboardTrends(BaseModel):
    outages_by_bank: list[NamedCount]
    outages_by_month: list[MonthlyCount]
    average_downtime_by_bank: list[AverageDowntime]
    planned_vs_unplanned: list[PlannedSplit]
