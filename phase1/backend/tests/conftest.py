import base64
import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


os.environ["AUTO_CREATE_TABLES"] = "false"
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["RATE_LIMIT_ENABLED"] = "false"

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import Bank, MaintenanceNotice, NPCIStatistic, Outage  # noqa: F401


engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


@pytest.fixture(autouse=True)
def reset_database() -> Generator[None, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def auth_headers() -> dict[str, str]:
    token = base64.b64encode(b"admin:admin123").decode("ascii")
    return {"Authorization": f"Basic {token}"}
