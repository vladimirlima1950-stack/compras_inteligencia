from fastapi import FastAPI, UploadFile, File
import pandas as pd
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

    try:

        caminho = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        # Salva o arquivo enviado
        with open(caminho, "wb") as f:
            f.write(await file.read())

        # Lê o arquivo
        if file.filename.lower().endswith(".csv"):

            try:
                df = pd.read_csv(
                    caminho,
                    sep=";",
                    dtype=str
                )

            except Exception:
                df = pd.read_csv(
                    caminho,
                    dtype=str
                )

        else:

            df = pd.read_excel(
                caminho,
                dtype=str
            )

        return {
            "status": "ok",
            "mensagem": "Arquivo recebido com sucesso",
            "arquivo": file.filename,
            "linhas": int(len(df)),
            "colunas": int(len(df.columns)),
            "nomes_colunas": [str(c) for c in df.columns]
        }

    except Exception as erro:

        return {
            "status": "erro",
            "mensagem": str(erro)
        }


@app.get("/processar_compras")
async def processar_compras(
    email: str,
    nome: str
):

    return {
        "status": "ok",
        "mensagem": "Processamento iniciado",
        "cliente": nome,
        "email": email
    }