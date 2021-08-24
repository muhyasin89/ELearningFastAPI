import sys

from fastapiproject.main import app
from starlette.testclient import TestClient

# app = FastAPI()


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
