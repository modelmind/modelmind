from starlette.testclient import TestClient
import pytest
from fastapi import FastAPI
from modelmind.api.business.app import app as main


@pytest.fixture(scope="module")
def test_client():
    with TestClient(main()) as client:
        yield client


@pytest.fixture(scope="module")
def app() -> FastAPI:
    return main()


def get_route_path(app: FastAPI, name: str) -> str:
    for route in app.routes:
        if route.name == name:  # type: ignore
            return route.path  # type: ignore
    raise ValueError(f"Route {name} not found")
