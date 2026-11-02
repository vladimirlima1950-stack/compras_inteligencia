from fastapi import FastAPI, UploadFile, File
from compras_inteligencia import processar_compras
import pandas as pd
import os

app = FastAPI(
    title="Compras Inteligência"
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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

    try:

        caminho = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(caminho, "wb") as f:
            f.write(await file.read())

        if file.filename.lower().endswith(".csv"):

            df = pd.read_csv(
                caminho,
                sep=None,
                engine="python"
            )

        elif file.filename.lower().endswith(".xlsx"):

            df = pd.read_excel(
                caminho,
                engine="openpyxl"
            )

        elif file.filename.lower().endswith(".xls"):

            df = pd.read_excel(
                caminho,
                engine="xlrd"
            )

        else:

            return {
                "status": "erro",
                "mensagem": "Formato não suportado."
            }

        return {
            "status": "ok",
            "mensagem": "Arquivo recebido com sucesso",
            "arquivo": file.filename,
            "linhas": int(len(df)),
            "colunas": int(len(df.columns))
        }

    except Exception as e:

        return {
            "status": "erro",
            "mensagem": str(e)
        }


@app.get("/processar_compras")
def executar_processamento(
    email: str,
    nome: str
):

    return processar_compras(
        email_cliente=email,
        nome_cliente=nome
    )