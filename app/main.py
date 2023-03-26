from fastapi import FastAPI
from api.endpoints import upload_csv
from db.database import create_tables

app = FastAPI()

create_tables()

app.include_router(upload_csv.router)

# Rota de status da API
@app.get("/status")
def status():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8008)
