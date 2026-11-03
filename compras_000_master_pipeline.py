# ============================================================
# COMPRAS INTELIGENCIA
# PIPELINE MESTRE
# ============================================================

from compras_010_valida_arquivo import (
    processar_compras as validar_arquivo
)

from compras_020_fato_compras import run as fato_compras


# ============================================================
# PIPELINE PRINCIPAL
# ============================================================

def processar_compras(
    email_cliente,
    nome_cliente
):

    resultado = validar_arquivo(
        email_cliente=email_cliente,
        nome_cliente=nome_cliente
    )

    if resultado["status"] != "ok":
        return resultado

    caminho_banco = (
        "compras_inteligencia.duckdb"
    )

    fato_compras(
        caminho_banco
    )

    return resultado