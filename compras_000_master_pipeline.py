#compras_000_master_pipeline.py

# ============================================================
# COMPRAS INTELIGENCIA
# PIPELINE MESTRE
# ============================================================

from compras_010_valida_arquivo import (
    processar_compras as validar_arquivo
)


# ============================================================
# PIPELINE PRINCIPAL
# ============================================================

def processar_compras_pipeline(
    email_cliente,
    nome_cliente
):

    return processar_compras(
        email_cliente=email_cliente,
        nome_cliente=nome_cliente
    )


# ============================================================
# COMPATIBILIDADE COM MAIN.PY
# ============================================================

def processar_compras(
    email_cliente,
    nome_cliente
):

    return processar_compras_pipeline(
        email_cliente=email_cliente,
        nome_cliente=nome_cliente
    )