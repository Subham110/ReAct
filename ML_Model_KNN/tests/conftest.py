"""
Shared test fixtures.

Provides a TestClient with lifespan enabled so models are loaded
before tests run, matching production behavior.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    """Create a TestClient that triggers the app lifespan (model loading)."""
    with TestClient(app) as c:
        yield c
