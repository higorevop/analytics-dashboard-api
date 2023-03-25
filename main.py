from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import csv
import io
from database import SessionLocal
from models import AnalyticsData
from database import create_tables

app = FastAPI()

@app.post("/upload", status_code=201)
async def upload_csv(file: UploadFile = File(...)):
    if file.content_type != "text/csv":
        return JSONResponse(status_code=400, content={"detail": "Invalid file format. Please upload a CSV file."})

    session = SessionLocal()
    try:
        csv_file = io.StringIO((await file.read()).decode("utf-8"))
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            analytics_data = AnalyticsData(
                review_time=int(row["review_time"]),
                team=row["team"],
                date=row["date"],
                merge_time=int(row["merge_time"])
            )
            session.add(analytics_data)

        session.commit()
        return {"detail": "Data uploaded successfully"}

    except Exception as e:
        session.rollback()
        return JSONResponse(status_code=500, content={"detail": f"Error occurred while processing the CSV file: {e}"})

    finally:
        session.close()