def test_summary_valid_group_id(client):
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n0,Application,2023-01-15,0\n715,Application,2023-01-16,597"
    files = {"file": ("sample.csv", csv_data, "text/csv")}
    upload_response = client.post("/upload_csv", files=files)
    assert upload_response.status_code == 201
    group_id = upload_response.json()["group_id"]

    response = client.get(f"/{group_id}/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["review_time"] == {
        "mean": 238.33333333333334, "median": 0.0, "mode": 0.0}
    assert data["merge_time"] == {"mean": 199.0, "median": 0.0, "mode": 0.0}


def test_summary_invalid_group_id(client):
    invalid_group_id = 999999
    response = client.get(f"/{invalid_group_id}/summary")
    assert response.status_code == 404
    assert response.json() == {"detail": "Group not found"}
