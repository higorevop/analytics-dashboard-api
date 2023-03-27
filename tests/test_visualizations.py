from urllib.parse import urlparse


def test_creation_and_sharing_line_chart(client):
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n0,Application,2023-01-15,0\n715,Application,2023-01-16,597"
    files = {"file": ("sample.csv", csv_data, "text/csv")}
    upload_response = client.post("/upload_csv", files=files)
    assert upload_response.status_code == 201
    group_id = upload_response.json()["group_id"]
    chart_type = "line_chart"
    response = client.get(f"/{group_id}/visualizations/{chart_type}")
    assert response.status_code == 200

    data = response.json()
    assert "chart_data" in data
    assert "share_url" in data

    share_url = data["share_url"]
    share_path = urlparse(share_url).path
    response = client.get(share_path)
    assert response.status_code == 200


def test_creation_and_sharing_bar_chart(client):
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n0,Application,2023-01-15,0\n715,Application,2023-01-16,597"
    files = {"file": ("sample.csv", csv_data, "text/csv")}
    upload_response = client.post("/upload_csv", files=files)
    assert upload_response.status_code == 201
    group_id = upload_response.json()["group_id"]
    chart_type = "bar_chart"
    response = client.get(f"/{group_id}/visualizations/{chart_type}")
    assert response.status_code == 200

    data = response.json()
    assert "chart_data" in data
    assert "share_url" in data

    share_url = data["share_url"]
    share_path = urlparse(share_url).path
    response = client.get(share_path)
    assert response.status_code == 200


def test_creation_and_sharing_scatter_plot(client):
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n0,Application,2023-01-15,0\n715,Application,2023-01-16,597"
    files = {"file": ("sample.csv", csv_data, "text/csv")}
    upload_response = client.post("/upload_csv", files=files)
    assert upload_response.status_code == 201
    group_id = upload_response.json()["group_id"]
    chart_type = "bar_chart"
    response = client.get(f"/{group_id}/visualizations/{chart_type}")
    assert response.status_code == 200

    data = response.json()
    assert "chart_data" in data
    assert "share_url" in data

    share_url = data["share_url"]
    share_path = urlparse(share_url).path
    response = client.get(share_path)
    assert response.status_code == 200


def test_creation_and_sharing_pie_chart(client):
    csv_data = "review_time,team,date,merge_time\n0,Application,2023-01-14,0\n0,Application,2023-01-15,0\n715,Application,2023-01-16,597"
    files = {"file": ("sample.csv", csv_data, "text/csv")}
    upload_response = client.post("/upload_csv", files=files)
    assert upload_response.status_code == 201
    group_id = upload_response.json()["group_id"]
    chart_type = "pie_chart"
    response = client.get(f"/{group_id}/visualizations/{chart_type}")
    assert response.status_code == 200

    data = response.json()
    assert "chart_data" in data
    assert "share_url" in data

    share_url = data["share_url"]
    share_path = urlparse(share_url).path
    response = client.get(share_path)
    assert response.status_code == 200
