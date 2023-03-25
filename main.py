import io
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import AnalyticsData, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

MAX_FILE_SIZE = 1024 * 1024 * 10  # 10 MB
REQUIRED_FIELDS = ["review_time", "team", "date", "merge_time"]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def read_file_content(file: UploadFile):
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


def validate_and_parse_csv(file_content):
    csv_file = io.StringIO(file_content.decode("utf-8"))
    df = pd.read_csv(csv_file)

    if not all(field in df.columns for field in REQUIRED_FIELDS):
        return JSONResponse(
            status_code=400,
            content={
                "detail": "Invalid CSV file. Please make sure all required fields are present in each row."
            },
        )

    if df.isnull().values.any():
        return JSONResponse(
            status_code=400,
            content={
                "detail": "Invalid CSV file. Please make sure all required fields are non-null values."
            },
        )

    df = df.astype({"review_time": "int32", "merge_time": "int32"})

    if not df.apply(lambda x: x.review_time >= 0 and x.merge_time >= 0, axis=1).all():
        return JSONResponse(
            status_code=400,
            content={
                "detail": "Invalid CSV file. Please make sure all required fields are valid non-negative integers and non-null values."
            },
        )

    data = [AnalyticsData(**row) for _, row in df.iterrows()]
    return data



@app.post("/upload", status_code=201)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "text/csv":
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid file format. Please upload a CSV file."},
        )

    file_content = await read_file_content(file)
    if file_content is None:
        return JSONResponse(
            status_code=400,
            content={"detail": "File too large. Please upload a smaller CSV file."},
        )

    if len(file_content) == 0:
        return JSONResponse(
            status_code=400,
            content={"detail": "Empty file. Please upload a non-empty CSV file."},
        )

    data = validate_and_parse_csv(file_content)
    if isinstance(data, JSONResponse):
        return data

    try:
        db.add_all(data)
        db.commit()
        return {"detail": "Data uploaded successfully"}

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error occurred while processing the CSV file: {e}"},
        )
