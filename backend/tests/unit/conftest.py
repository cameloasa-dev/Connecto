import pytest


@pytest.fixture
def fake_user():
    return {"id": 1, "username": "test_user"}
