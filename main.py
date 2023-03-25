from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import JSONResponse
import csv
import io
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import AnalyticsData, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.post("/upload", status_code=201)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "text/csv":
        return JSONResponse(status_code=400, content={"detail": "Invalid file format. Please upload a CSV file."})

    file_content = await file.read()
    if len(file_content) == 0:
        return JSONResponse(status_code=400, content={"detail": "Empty file. Please upload a non-empty CSV file."})

    try:
        csv_file = io.StringIO(file_content.decode("utf-8"))
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            analytics_data = AnalyticsData(
                review_time=int(row["review_time"]),
                team=row["team"],
                date=row["date"],
                merge_time=int(row["merge_time"])
            )
            db.add(analytics_data)

        db.commit()
        return {"detail": "Data uploaded successfully"}

    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"detail": f"Error occurred while processing the CSV file: {e}"})
