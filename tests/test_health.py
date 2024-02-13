from tests.conftest import get_route_path
from starlette.testclient import TestClient
from fastapi import FastAPI


def test_health_check(test_client: TestClient, app: FastAPI) -> None:
    endpoint_path = get_route_path(app, "health_check")
    response = test_client.get(endpoint_path)
    assert response.status_code == 200
