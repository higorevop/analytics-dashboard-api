import uvicorn

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")
