"""Test router for health check."""
from fastapi.testclient import TestClient

from main import main_app

client = TestClient(main_app)


def test_health_check_for_main_app():
    """Test health check endpoint for main app (root app)."""
    response = client.get("/health-check")
    assert response.status_code == 200
    assert response.json() == {"message": "Alive and well!"}


def test_health_check_for_app_v1():
    """Test health check endpoint for v1 of app."""
    # Intentionally hard code /api/v1 rather than importing v1_router.prefix from main.py.
    # This will ensure that this test fails if there are any path changes.
    response = client.get("/api/v1/health-check")
    assert response.status_code == 200
    assert response.json() == {"message": "Alive and well!"}
