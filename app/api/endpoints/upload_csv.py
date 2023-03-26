from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import engine, Base
from db.database import get_db
from utils.csv import (
    read_file_content,
    validate_and_parse_csv,
    ERROR_MESSAGES
)
from db.models import AnalyticsDataGroup
from datetime import datetime
from utils.analytics_db import calculate_and_store_summary
from typing import List, Union

Base.metadata.create_all(bind=engine)

class UploadResponse(BaseModel):
    detail: str
    group_id: int

router = APIRouter()

@router.post("/upload_csv", status_code=201, response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(..., description="The CSV file to upload (multipart/form-data)"),
                     db: Session = Depends(get_db)) -> Union[UploadResponse, JSONResponse]:
    """
    Upload CSV

    Upload a CSV file containing columns review_time, team, date, and merge_time.
    """
    if file.content_type != "text/csv":
        return JSONResponse(
            status_code=400,
            content={"detail": ERROR_MESSAGES["invalid_file_format"]},
        )

    file_content: str = await read_file_content(file)
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

    analytics_data_group: AnalyticsDataGroup = AnalyticsDataGroup(created_at=datetime.utcnow())
    db.add(analytics_data_group)
    db.commit()

    data: Union[list, JSONResponse] = validate_and_parse_csv(file_content, analytics_data_group.id)
    if isinstance(data, JSONResponse):
        return data

    analytics_data_group: AnalyticsDataGroup = AnalyticsDataGroup(created_at=datetime.utcnow())
    db.add(analytics_data_group)
    db.commit()

    data: Union[list, JSONResponse] = validate_and_parse_csv(file_content, analytics_data_group.id)
    if isinstance(data, JSONResponse):
        return data

    try:
        db.add_all(data)
        db.commit()
        calculate_and_store_summary(db, analytics_data_group, data)

        return UploadResponse(detail=ERROR_MESSAGES["upload_successful"], group_id=analytics_data_group.id)
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"detail": ERROR_MESSAGES["processing_error"].format(error=e)},
        )
