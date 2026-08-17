from fastapi.testclient import TestClient
import base64

def test_health_endpoint(client: TestClient):
    creds = base64.b64encode(b"testuser:testpass").decode("utf-8")
    response = client.get(                          # type: ignore
        "/demo/health",
        headers={"Authorization":f"Basic {creds}"}
        )
    assert response.status_code == 200              # type: ignore
    assert response.json() == {"status": "ok"}      # type: ignore
