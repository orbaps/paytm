from datetime import datetime

from pydantic import Field, model_validator

from .common import ORMModel


class MaintenanceNoticeBase(ORMModel):
    bank_id: int
    title: str = Field(min_length=2, max_length=180)
    description: str = Field(min_length=2)
    maintenance_start: datetime
    maintenance_end: datetime
    source: str = Field(min_length=2, max_length=240)

    @model_validator(mode="after")
    def validate_time_window(self) -> "MaintenanceNoticeBase":
        if self.maintenance_end < self.maintenance_start:
            raise ValueError("maintenance_end must be after maintenance_start")
        return self


class MaintenanceNoticeCreate(MaintenanceNoticeBase):
    pass


class MaintenanceNoticeUpdate(ORMModel):
    bank_id: int | None = None
    title: str | None = Field(default=None, min_length=2, max_length=180)
    description: str | None = Field(default=None, min_length=2)
    maintenance_start: datetime | None = None
    maintenance_end: datetime | None = None
    source: str | None = Field(default=None, min_length=2, max_length=240)


class MaintenanceNoticeRead(MaintenanceNoticeBase):
    id: int
    created_at: datetime
