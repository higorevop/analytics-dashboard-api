from fastapi import FastAPI, Depends
from starlette.requests import Request
from starlette.responses import Response
from api.endpoints import upload_csv, analytics, visualizations
from db.database import create_tables, database

app: FastAPI = FastAPI(title="Analytics Dashboard API", version="0.1.0")

@app.on_event("startup")
async def startup() -> None:
    await database.connect()
    await create_tables()  

@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()

app.include_router(upload_csv.router)
app.include_router(analytics.router)
app.include_router(visualizations.router)

app.openapi()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
