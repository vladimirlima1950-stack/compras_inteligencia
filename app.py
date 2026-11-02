from fastapi import FastAPI, UploadFile, File
import os

app = FastAPI()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {
        "status": "ok",
        "modulo": "Inteligencia de Compras"
    }

@app.post("/upload_compras")
async def upload_compras(file: UploadFile = File(...)):

    caminho = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(caminho, "wb") as f:
        f.write(await file.read())

    return {
        "status": "ok",
        "mensagem": "Arquivo recebido com sucesso"
    }

@app.get("/processar_compras")
async def processar_compras(email: str, nome: str):

    return {
        "status": "ok",
        "mensagem": "Processamento iniciado",
        "cliente": nome,
        "email": email
    }