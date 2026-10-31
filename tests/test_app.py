
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["status"] == "running"


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_create_payment_success(client):
    response = client.post(
        "/payments",
        json={
            "amount": 100,
            "currency": "INR"
        }
    )

    assert response.status_code == 201
    assert response.json["status"] == "SUCCESS"
    assert response.json["amount"] == 100
    assert response.json["currency"] == "INR"
    assert "payment_id" in response.json


def test_create_payment_missing_amount(client):
    response = client.post(
        "/payments",
        json={
            "currency": "INR"
        }
    )

    assert response.status_code == 400


def test_create_payment_invalid_amount(client):
    response = client.post(
        "/payments",
        json={
            "amount": -100,
            "currency": "INR"
        }
    )

    assert response.status_code == 400


def test_create_payment_invalid_json(client):
    response = client.post(
        "/payments",
        data="invalid-json",
        content_type="application/json"
    )

    assert response.status_code == 400