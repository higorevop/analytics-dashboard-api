def test_summary_valid_group_id(client):
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n0,Application,2023-01-15,0\n715,Application,2023-01-16,597"
    files = {"file": ("sample.csv", csv_data, "text/csv")}
    upload_response = client.post("/upload_csv", files=files)
    assert upload_response.status_code == 201
    group_id = upload_response.json()["group_id"]

    response = client.get(f"/summary/{group_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["mean"] == {"review_time": 238.33333333333334, "merge_time": 199.0}
    assert data["median"] == {"review_time": 0, "merge_time": 0}
    assert data["mode"] == {"review_time": [0], "merge_time": [0]}


def test_summary_invalid_group_id(client):
    invalid_group_id = 999999
    response = client.get(f"/summary/{invalid_group_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Group not found"}

