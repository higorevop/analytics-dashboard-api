import pytest
from fastapi.testclient import TestClient
from main import app
from database import create_tables, drop_tables

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    create_tables()
    yield
    drop_tables()

def test_upload_csv():
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n0,Application,2023-01-15,0\n715,Application,2023-01-16,597"
    files = {"file": ("sample.csv", csv_data, "text/csv")}
    response = client.post("/upload", files=files)
    assert response.status_code == 201, f"Response: {response.text}"
    assert response.json() == {"detail": "Data uploaded successfully"}
