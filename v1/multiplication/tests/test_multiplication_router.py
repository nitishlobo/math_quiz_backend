"""Test router for multiplication."""
from fastapi.testclient import TestClient

from main import main_app, v1_router

client = TestClient(main_app)


def test_create_multiplication_dataset():
    """Test create multiplication dataset."""
    response = client.post(f"{v1_router.prefix}/multiplication")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
