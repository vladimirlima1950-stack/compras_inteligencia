from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "ok",
        "modulo": "Inteligencia de Compras"
    }

@app.post("/upload_compras")
async def upload_compras(
    file: UploadFile = File(...)
):
    return {
        "status": "ok",
        "arquivo_recebido": file.filename
    }