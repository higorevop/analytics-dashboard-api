from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.database import engine
from db.database import get_db
from utils.csv import (
    read_file_content,
    validate_and_parse_csv,
    ERROR_MESSAGES)
from db.database import Base
from db.models import AnalyticsDataGroup, AnalyticsData
from datetime import datetime

Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.post("/upload_csv", status_code=201)
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

    analytics_data_group = AnalyticsDataGroup(created_at=datetime.utcnow())
    db.add(analytics_data_group)
    db.commit()

    data = validate_and_parse_csv(file_content, analytics_data_group.id)
    if isinstance(data, JSONResponse):
        return data

    try:
        db.add_all(data)
        db.commit()
        return {"detail": ERROR_MESSAGES["upload_successful"], "group_id": analytics_data_group.id}
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"detail": ERROR_MESSAGES["processing_error"].format(error=e)},
        )
