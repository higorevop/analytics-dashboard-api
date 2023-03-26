import pytest


def test_upload_csv(client, error_messages):
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n0,Application,2023-01-15,0\n715,Application,2023-01-16,597"
    files = {"file": ("sample.csv", csv_data, "text/csv")}
    response = client.post("/upload_csv", files=files)
    assert response.status_code == 201, f"Response: {response.text}"
    assert response.json() == {"detail": error_messages["upload_successful"]}


def test_upload_empty_csv(client, error_messages):
    csv_data = ""
    files = {"file": ("empty.csv", csv_data, "text/csv")}
    response = client.post("/upload_csv", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": error_messages["empty_file"]}


def test_upload_invalid_csv(client, error_messages):
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n0,Application,2023-01-15\n715,Application,2023-01-16,597"
    files = {"file": ("invalid.csv", csv_data, "text/csv")}
    response = client.post("/upload_csv", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": error_messages["invalid_csv"]}


def test_upload_large_csv(client, error_messages):
    csv_data = "review_time,team,date,merge_time\n" + "0,Application,2023-01-14,0\n" * 1000000 + "0,Application,2023-01-15,0\n715,Application,2023-01-16,597"
    files = {"file": ("large.csv", csv_data, "text/csv")}
    response = client.post("/upload_csv", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": error_messages["file_too_large"]}


def test_upload_non_csv_file(client, error_messages):
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n0,Application,2023-01-15,0\n715,Application,2023-01-16,597"
    files = {"file": ("sample.txt", csv_data, "text/plain")}
    response = client.post("/upload_csv", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": error_messages["invalid_file_format"]}


def test_upload_csv_with_negative_values(client, error_messages):
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n-1,Application,2023-01-15,0\n715,Application,2023-01-16,-597"
    files = {"file": ("negative_values.csv", csv_data, "text/csv")}
    response = client.post("/upload_csv", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": error_messages["invalid_csv"]}


def test_upload_csv_with_additional_fields(client, error_messages):
    csv_data = "review_time,team,date,merge_time,extra_field\n0,Application,2023-01-14,0,100\n0,Application,2023-01-15,0,200\n715,Application,2023-01-16,597,300"
    files = {"file": ("additional_fields.csv", csv_data, "text/csv")}
    response = client.post("/upload_csv", files=files)
    assert response.status_code == 201, f"Response: {response.text}"
    assert response.json() == {"detail": error_messages["upload_successful"]}


def test_upload_csv_with_missing_fields(client, error_messages):
    csv_data = "review_time,date,merge_time\n0,2023-01-14,0\n0,2023-01-15,0\n715,2023-01-16,597"
    files = {"file": ("missing_fields.csv", csv_data, "text/csv")}
    response = client.post("/upload_csv", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": error_messages["invalid_csv"]}


def test_upload_csv_with_invalid_date_format(client, error_messages):
    csv_data = "review_time,team,date,merge_time\n0,Application,14/01/2023,0\n0,Application,15/01/2023,0\n715,Application,16/01/2023,597"
    files = {"file": ("invalid_date_format.csv", csv_data, "text/csv")}
    response = client.post("/upload_csv", files=files)
    assert response.status_code == 400, f"Response: {response.text}"
    assert response.json() == {"detail": error_messages["invalid_date_format"]}

 