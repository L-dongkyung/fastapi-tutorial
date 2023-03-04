from fastapi.testclient import TestClient

from main import app


def test_websocket():
    test_client = TestClient(app)
    with test_client.websocket_connect("/advanced/ws/123") as ws:
        ws.send_text("asdf")
        data = ws.receive_text()
        assert data == "You wrote: asdf"
