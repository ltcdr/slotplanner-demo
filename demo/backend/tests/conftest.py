import pytest
from pytest import MonkeyPatch


# --- IMPORT FASTAPI APP ------------------------------------------------------
try:
    # Running inside the meta repo
    from services.slotplanner_demo.demo.backend.main import app
except ModuleNotFoundError:
    # Running inside the standalone submodule
    from demo.backend.main import app

from fastapi.testclient import TestClient


# --- FIXTURES ----------------------------------------------------------------
@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def test_credentials(monkeypatch: MonkeyPatch):
    monkeypatch.setenv("DEMO_USERNAME", "testuser")
    monkeypatch.setenv("DEMO_PASSWORD", "testpass")


class FakeSession:
    def commit(self): pass
    def rollback(self): pass
    def close(self): pass


@pytest.fixture
def mock_db(monkeypatch: MonkeyPatch):
    def fake_get_db():
        yield FakeSession()

    try:
        # Meta repo path
        monkeypatch.setattr(
            "services.slotplanner_demo.demo.backend.db.get_db",
            fake_get_db
        )
    except ModuleNotFoundError:
        # Standalone submodule path
        monkeypatch.setattr(
            "demo.backend.db.get_db",
            fake_get_db
        )


@pytest.fixture
def env(monkeypatch: MonkeyPatch):
    monkeypatch.setenv("SLOTPLANNER_ENV", "test")
