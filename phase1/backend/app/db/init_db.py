from sqlalchemy import Engine

from app.db.base import Base
from app.models import bank, maintenance_notice, npci_statistic, outage  # noqa: F401


def init_db(engine: Engine) -> None:
    Base.metadata.create_all(bind=engine)
