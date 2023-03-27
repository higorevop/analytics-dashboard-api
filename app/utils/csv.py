import io
import datetime
from typing import List, Union, Dict
import pandas as pd
from fastapi.responses import JSONResponse
from db.models import AnalyticsData
from fastapi import UploadFile
from datetime import date


MAX_FILE_SIZE: int = 1024 * 1024 * 10  # 10 MB
REQUIRED_FIELDS: List[str] = ["review_time", "team", "date", "merge_time"]
ERROR_MESSAGES: Dict[str, str] = {
    "invalid_csv": "Invalid CSV file. Please make sure all required fields are present in each row.",
    "invalid_date_format": "Invalid date format. Please make sure all date values are in the format YYYY-MM-DD.",
    "invalid_file_format": "Invalid file format. Please upload a CSV file.",
    "file_too_large": "File too large. Please upload a smaller CSV file.",
    "empty_file": "Empty file. Please upload a non-empty CSV file.",
    "upload_successful": "Data uploaded successfully",
    "processing_error": "Error occurred while processing the CSV file: {error}",
}


async def read_file_content(file: UploadFile) -> Union[bytes, None]:
    file_size: int = 0
    file_content: bytes = b""
    while True:
        chunk: bytes = await file.read(10000)
        if not chunk:
            break
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE:
            return None
        file_content += chunk
    return file_content


def is_valid_date(date_str: str) -> bool:
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_and_parse_csv(file_content: bytes, group_id: int) -> Union[List[AnalyticsData], JSONResponse]:
    csv_file: io.StringIO = io.StringIO(file_content.decode("utf-8"))
    df: pd.DataFrame = pd.read_csv(csv_file)

    if not all(field in df.columns for field in REQUIRED_FIELDS):
        return JSONResponse(
            status_code=400,
            content={"detail": ERROR_MESSAGES["invalid_csv"]},
        )

    df = df[REQUIRED_FIELDS]

    if not df["date"].apply(is_valid_date).all():
        return JSONResponse(
            status_code=400,
            content={"detail": ERROR_MESSAGES["invalid_date_format"]},
        )

    if df.isnull().values.any():
        return JSONResponse(
            status_code=400,
            content={"detail": ERROR_MESSAGES["invalid_csv"]},
        )

    df = df.astype({"review_time": "int32", "merge_time": "int32"})

    if not df.apply(lambda x: x.review_time >= 0 and x.merge_time >= 0, axis=1).all():
        return JSONResponse(
            status_code=400,
            content={"detail": ERROR_MESSAGES["invalid_csv"]},
        )

    data: List[AnalyticsData] = [AnalyticsData(
        group_id=group_id, **row) for _, row in df.iterrows()]
    return data


def analytics_data_to_dict(analytics_data: AnalyticsData) -> dict:
    return {
        "review_time": analytics_data.review_time,
        "team": analytics_data.team,
        "date": date.fromisoformat(analytics_data.date) if isinstance(analytics_data.date, str) else analytics_data.date,
        "merge_time": analytics_data.merge_time,
        "group_id": analytics_data.group_id
    }
