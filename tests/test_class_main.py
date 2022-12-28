import logging
import time

from fastapi.testclient import TestClient

from main import app

class TestMain:

    start_time = 0

    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)
        cls.start_time = time.time()

    @classmethod
    def teardown_class(cls):
        logging.info(f"test end. process_time: {time.time() - cls.start_time}")

    def test_read_main(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}