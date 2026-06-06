from datetime import datetime
from decimal import Decimal

from pydantic import Field

from .common import ORMModel


class NPCIStatisticBase(ORMModel):
    bank_id: int
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=2000, le=2100)
    success_rate: Decimal = Field(ge=0, le=100, max_digits=5, decimal_places=2)
    technical_decline: Decimal = Field(ge=0, le=100, max_digits=5, decimal_places=2)
    business_decline: Decimal = Field(ge=0, le=100, max_digits=5, decimal_places=2)
    source: str = Field(default="manual", min_length=2, max_length=240)


class NPCIStatisticCreate(NPCIStatisticBase):
    pass


class NPCIStatisticUpdate(ORMModel):
    bank_id: int | None = None
    month: int | None = Field(default=None, ge=1, le=12)
    year: int | None = Field(default=None, ge=2000, le=2100)
    success_rate: Decimal | None = Field(default=None, ge=0, le=100, max_digits=5, decimal_places=2)
    technical_decline: Decimal | None = Field(default=None, ge=0, le=100, max_digits=5, decimal_places=2)
    business_decline: Decimal | None = Field(default=None, ge=0, le=100, max_digits=5, decimal_places=2)
    source: str | None = Field(default=None, min_length=2, max_length=240)


class NPCIStatisticRead(NPCIStatisticBase):
    id: int
    created_at: datetime
