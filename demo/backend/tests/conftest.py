import sys
from pathlib import Path
import pytest
from pytest import MonkeyPatch


# --- PATH SETUP --------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]

SERVICE_ROOT = ROOT / "services" / "slotplanner_demo"
DEMO_ROOT = SERVICE_ROOT / "demo"
BACKEND_ROOT = DEMO_ROOT / "backend"

sys.path.append(str(ROOT))
sys.path.append(str(SERVICE_ROOT))
sys.path.append(str(DEMO_ROOT))
sys.path.append(str(BACKEND_ROOT))


# --- IMPORT FASTAPI APP ------------------------------------------------------
from services.slotplanner_demo.demo.backend.main import app
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

    monkeypatch.setattr(
        "services.slotplanner_demo.demo.backend.db.get_db",
        fake_get_db
    )


@pytest.fixture
def env(monkeypatch: MonkeyPatch):
    monkeypatch.setenv("SLOTPLANNER_ENV", "test")
