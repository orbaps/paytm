from datetime import datetime

from pydantic import Field

from .common import ORMModel


class BankBase(ORMModel):
    bank_name: str = Field(min_length=2, max_length=160)
    bank_type: str = Field(min_length=2, max_length=80)
    upi_enabled: bool = True


class BankCreate(BankBase):
    pass


class BankUpdate(ORMModel):
    bank_name: str | None = Field(default=None, min_length=2, max_length=160)
    bank_type: str | None = Field(default=None, min_length=2, max_length=80)
    upi_enabled: bool | None = None


class BankRead(BankBase):
    id: int
    created_at: datetime
