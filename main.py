from fastapi import FastAPI, UploadFile, File
from compras_000_master_pipeline import processar_compras
import pandas as pd
import os

app = FastAPI(
    title="Compras Inteligência"
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def normalizar_idioma(idioma: str | None) -> str:
    idioma_limpo = (idioma or "PT").strip().upper()
    if idioma_limpo not in {"PT", "EN"}:
        return "PT"
    return idioma_limpo


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
        nome_seguro = os.path.basename(file.filename or "")
        if not nome_seguro:
            return {
                "status": "erro",
                "mensagem": "Nome de arquivo inválido."
            }

        caminho = os.path.join(
            UPLOAD_DIR,
            nome_seguro
        )

        with open(caminho, "wb") as f:
            f.write(await file.read())

        extensao = nome_seguro.lower()

        if extensao.endswith(".csv"):
            df = pd.read_csv(
                caminho,
                sep=None,
                engine="python"
            )
        elif extensao.endswith(".xlsx"):
            df = pd.read_excel(
                caminho,
                engine="openpyxl"
            )
        elif extensao.endswith(".xls"):
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
            "arquivo": nome_seguro,
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
    nome: str,
    idioma: str = "PT"
):
    idioma_validado = normalizar_idioma(idioma)
    return processar_compras(
        email_cliente=email,
        nome_cliente=nome,
        idioma=idioma_validado
    )