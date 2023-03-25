import pytest
from fastapi.testclient import TestClient
from database import create_tables, drop_tables
from main import app

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

def test_upload_empty_csv():
    csv_data = ""
    files = {"file": ("empty.csv", csv_data, "text/csv")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": "Empty file. Please upload a non-empty CSV file."}

def test_upload_invalid_csv():
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n0,Application,2023-01-15\n715,Application,2023-01-16,597"
    files = {"file": ("invalid.csv", csv_data, "text/csv")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": "Invalid CSV file. Please make sure all required fields are non-null values."}


def test_upload_large_csv():
    csv_data = "review_time,team,date,merge_time\n" + "0,Application,2023-01-14,0\n" * 1000000 + "0,Application,2023-01-15,0\n715,Application,2023-01-16,597"
    files = {"file": ("large.csv", csv_data, "text/csv")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": "File too large. Please upload a smaller CSV file."}

def test_upload_non_csv_file():
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n0,Application,2023-01-15,0\n715,Application,2023-01-16,597"
    files = {"file": ("sample.txt", csv_data, "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": "Invalid file format. Please upload a CSV file."}
