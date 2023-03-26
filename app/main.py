from databases import Database 
from fastapi import FastAPI
from api.endpoints import upload_csv, analytics, visualizations
from db.database import create_tables

app: FastAPI = FastAPI(title="Analytics Dashboard API", version="0.1.0")

@app.on_event("startup")
async def startup() -> None:
    await create_tables()  

app.include_router(upload_csv.router)
app.include_router(analytics.router)
app.include_router(visualizations.router)
app.openapi() 

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8088)
