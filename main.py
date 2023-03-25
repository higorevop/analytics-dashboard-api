import io
import datetime
from typing import List, Union, Dict

import pandas as pd
from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import AnalyticsData, Base
import logging


Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)

app = FastAPI()

MAX_FILE_SIZE = 1024 * 1024 * 10  # 10 MB
REQUIRED_FIELDS = ["review_time", "team", "date", "merge_time"]
ERROR_MESSAGES: Dict[str, str] = {
    "invalid_csv": "Invalid CSV file. Please make sure all required fields are present in each row.",
    "invalid_date_format": "Invalid date format. Please make sure all date values are in the format YYYY-MM-DD.",
    "invalid_null_values": "Invalid CSV file. Please make sure all required fields are non-null values.",
    "invalid_integers": "Invalid CSV file. Please make sure all required fields are valid non-negative integers and non-null values.",
    "invalid_file_format": "Invalid file format. Please upload a CSV file.",
    "file_too_large": "File too large. Please upload a smaller CSV file.",
    "empty_file": "Empty file. Please upload a non-empty CSV file.",
    "upload_successful": "Data uploaded successfully",
    "processing_error": "Error occurred while processing the CSV file: {error}",
}


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def read_file_content(file: UploadFile) -> Union[bytes, None]:
    file_size = 0
    file_content = b""
    while True:
        chunk = await file.read(10000)
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


def validate_and_parse_csv(file_content: bytes) -> Union[List[AnalyticsData], JSONResponse]:
    csv_file = io.StringIO(file_content.decode("utf-8"))
    df = pd.read_csv(csv_file)

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
            content={"detail": ERROR_MESSAGES["invalid_null_values"]},
        )

    df = df.astype({"review_time": "int32", "merge_time": "int32"})

    if not df.apply(lambda x: x.review_time >= 0 and x.merge_time >= 0, axis=1).all():
        return JSONResponse(
            status_code=400,
            content={"detail": ERROR_MESSAGES["invalid_integers"]},
        )

    data = [AnalyticsData(**row) for _, row in df.iterrows()]
    return data


@app.post("/upload", status_code=201)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "text/csv":
        return JSONResponse(
            status_code=400,
            content={"detail": ERROR_MESSAGES["invalid_file_format"]},
        )

    file_content = await read_file_content(file)
    if file_content is None:
        return JSONResponse(
            status_code=400,
            content={"detail": ERROR_MESSAGES["file_too_large"]},
        )

    if len(file_content) == 0:
        return JSONResponse(
            status_code=400,
            content={"detail": ERROR_MESSAGES["empty_file"]},
        )

    data = validate_and_parse_csv(file_content)
    if isinstance(data, JSONResponse):
        return data

    try:
        db.add_all(data)
        db.commit()
        return {"detail": ERROR_MESSAGES["upload_successful"]}
    except Exception as e:
        db.rollback()
    return JSONResponse(
        status_code=500,
        content={"detail": ERROR_MESSAGES["processing_error"].format(error=e)},
    )
