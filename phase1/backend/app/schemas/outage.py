from datetime import datetime

from pydantic import Field, model_validator

from .common import ORMModel


class OutageBase(ORMModel):
    bank_id: int
    outage_type: str = Field(min_length=2, max_length=80)
    planned: bool = False
    severity: str = Field(min_length=2, max_length=40)
    start_time: datetime
    end_time: datetime
    duration_minutes: int | None = Field(default=None, ge=0)
    source: str = Field(min_length=2, max_length=240)

    @model_validator(mode="after")
    def validate_time_window(self) -> "OutageBase":
        if self.end_time < self.start_time:
            raise ValueError("end_time must be after start_time")
        if self.duration_minutes is None:
            self.duration_minutes = int((self.end_time - self.start_time).total_seconds() // 60)
        return self


class OutageCreate(OutageBase):
    pass


class OutageUpdate(ORMModel):
    bank_id: int | None = None
    outage_type: str | None = Field(default=None, min_length=2, max_length=80)
    planned: bool | None = None
    severity: str | None = Field(default=None, min_length=2, max_length=40)
    start_time: datetime | None = None
    end_time: datetime | None = None
    duration_minutes: int | None = Field(default=None, ge=0)
    source: str | None = Field(default=None, min_length=2, max_length=240)


class OutageRead(OutageBase):
    id: int
    created_at: datetime
