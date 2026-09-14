"""
Pytest configuration and fixtures for Call_ML_Model backend.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="session")
def client():
    """Session-scoped TestClient with lifespan context."""
    with TestClient(app) as test_client:
        yield test_client
