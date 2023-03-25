import pytest
from fastapi.testclient import TestClient
from database import create_tables, drop_tables
from main import app

client = TestClient(app)

ERROR_MESSAGES = {
    "invalid_file_format": "Invalid file format. Please upload a CSV file.",
    "empty_file": "Empty file. Please upload a non-empty CSV file.",
    "invalid_csv": "Invalid CSV file. Please make sure all required fields are non-null values.",
    "file_too_large": "File too large. Please upload a smaller CSV file.",
    "invalid_values": "Invalid CSV file. Please make sure all required fields are valid non-negative integers and non-null values.",
    "missing_fields": "Invalid CSV file. Please make sure all required fields are present in each row.",
    "invalid_date_format": "Invalid date format. Please make sure all date values are in the format YYYY-MM-DD.",
    "upload_successful": "Data uploaded successfully",
}


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
    assert response.json() == {"detail": ERROR_MESSAGES["upload_successful"]}


def test_upload_empty_csv():
    csv_data = ""
    files = {"file": ("empty.csv", csv_data, "text/csv")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": ERROR_MESSAGES["empty_file"]}


def test_upload_invalid_csv():
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n0,Application,2023-01-15\n715,Application,2023-01-16,597"
    files = {"file": ("invalid.csv", csv_data, "text/csv")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": ERROR_MESSAGES["invalid_csv"]}


def test_upload_large_csv():
    csv_data = "review_time,team,date,merge_time\n" + "0,Application,2023-01-14,0\n" * 1000000 + "0,Application,2023-01-15,0\n715,Application,2023-01-16,597"
    files = {"file": ("large.csv", csv_data, "text/csv")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": ERROR_MESSAGES["file_too_large"]}


def test_upload_non_csv_file():
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n0,Application,2023-01-15,0\n715,Application,2023-01-16,597"
    files = {"file": ("sample.txt", csv_data, "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": ERROR_MESSAGES["invalid_file_format"]}


def test_upload_csv_with_negative_values():
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n-1,Application,2023-01-15,0\n715,Application,2023-01-16,-597"
    files = {"file": ("negative_values.csv", csv_data, "text/csv")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": ERROR_MESSAGES["invalid_values"]}


def test_upload_csv_with_additional_fields():
    csv_data = "review_time,team,date,merge_time,extra_field\n0,Application,2023-01-14,0,100\n0,Application,2023-01-15,0,200\n715,Application,2023-01-16,597,300"
    files = {"file": ("additional_fields.csv", csv_data, "text/csv")}
    response = client.post("/upload", files=files)
    assert response.status_code == 201, f"Response: {response.text}"
    assert response.json() == {"detail": ERROR_MESSAGES["upload_successful"]}


def test_upload_csv_with_missing_fields():
    csv_data = "review_time,date,merge_time\n0,2023-01-14,0\n0,2023-01-15,0\n715,2023-01-16,597"
    files = {"file": ("missing_fields.csv", csv_data, "text/csv")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": ERROR_MESSAGES["missing_fields"]}


def test_upload_csv_with_invalid_date_format():
    csv_data = "review_time,team,date,merge_time\n0,Application,14/01/2023,0\n0,Application,15/01/2023,0\n715,Application,16/01/2023,597"
    files = {"file": ("invalid_date_format.csv", csv_data, "text/csv")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": ERROR_MESSAGES["invalid_date_format"]}
