from datetime import datetime, timedelta, timezone


def test_health_is_public(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["phase"] == "1"


def test_bank_crud(client, auth_headers):
    create_response = client.post(
        "/api/banks",
        headers=auth_headers,
        json={"bank_name": "HDFC Bank", "bank_type": "private_sector", "upi_enabled": True},
    )

    assert create_response.status_code == 201
    bank_id = create_response.json()["id"]

    list_response = client.get("/api/banks", headers=auth_headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.put(
        f"/api/banks/{bank_id}",
        headers=auth_headers,
        json={"bank_type": "private_sector_bank"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["bank_type"] == "private_sector_bank"

    delete_response = client.delete(f"/api/banks/{bank_id}", headers=auth_headers)
    assert delete_response.status_code == 200
    assert delete_response.json() == {"deleted": True, "id": bank_id}


def test_outage_create_and_dashboard_summary(client, auth_headers):
    bank = client.post(
        "/api/banks",
        headers=auth_headers,
        json={"bank_name": "Axis Bank", "bank_type": "private_sector", "upi_enabled": True},
    ).json()
    start = datetime(2026, 1, 5, 10, 0, tzinfo=timezone.utc)
    end = start + timedelta(minutes=45)

    outage_response = client.post(
        "/api/outages",
        headers=auth_headers,
        json={
            "bank_id": bank["id"],
            "outage_type": "upi",
            "planned": False,
            "severity": "high",
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "source": "unit test",
        },
    )

    assert outage_response.status_code == 201
    assert outage_response.json()["duration_minutes"] == 45

    summary = client.get("/api/dashboard/summary", headers=auth_headers).json()
    assert summary["bank_count"] == 1
    assert summary["outage_count"] == 1
    assert summary["unplanned_outage_count"] == 1


def test_json_import_for_banks(client, auth_headers):
    payload = b'[{"bank_name":"ICICI Bank","bank_type":"private_sector","upi_enabled":true}]'

    response = client.post(
        "/api/imports/banks",
        headers=auth_headers,
        files={"file": ("banks.json", payload, "application/json")},
    )

    assert response.status_code == 200
    assert response.json()["imported"] == 1

    banks = client.get("/api/banks", headers=auth_headers).json()
    assert banks[0]["bank_name"] == "ICICI Bank"


def test_api_requires_auth(client):
    response = client.get("/api/banks")

    assert response.status_code == 401
