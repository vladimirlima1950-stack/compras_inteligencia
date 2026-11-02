from fastapi import FastAPI
from compras_inteligencia import processar_compras

app = FastAPI(
    title="Compras Inteligência"
)


@app.get("/")
def home():

    return {
        "status": "ok",
        "modulo": "Inteligencia de Compras"
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