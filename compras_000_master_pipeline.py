# ============================================================
# COMPRAS INTELIGENCIA
# PIPELINE MESTRE
# ============================================================

from compras_010_valida_arquivo import (
    processar_compras as validar_arquivo
)

from compras_020_fato_compras import run as fato_compras

from compras_030_dim_calendario import (
    run as dim_calendario
)

from compras_040_compras_mensais import (
    run as compras_mensais
)

from compras_050_produto_mes import (
    run as produto_mes
)

from compras_060_fornecedor_mes import (
    run as fornecedor_mes
)


from compras_070_produto_fornecedor_mes import (
    run as produto_fornecedor_mes
)

from compras_100_resumo_executivo import (
    run as resumo_executivo
)

from compras_110_ranking_fornecedores import (
    run as ranking_fornecedores
)

from compras_120_curva_abc_fornecedores import (
    run as curva_abc_fornecedores
)


from compras_130_ranking_produtos import (
    run as ranking_produtos
)


from compras_140_curva_abc_produtos import (
    run as curva_abc_produtos
)

from compras_150_evolucao_custos import (
    run as evolucao_custos
)




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

    dim_calendario(
        caminho_banco
    )


    compras_mensais(
        caminho_banco
    )

    produto_mes(
        caminho_banco
    )

    fornecedor_mes(
        caminho_banco
    )

    produto_fornecedor_mes(
        caminho_banco
    )

    resumo_executivo(
        caminho_banco
    )

    ranking_fornecedores(
        caminho_banco
    )


    curva_abc_fornecedores(
        caminho_banco
    )

    ranking_produtos(
        caminho_banco
    )

    curva_abc_produtos(
        caminho_banco
    )

    evolucao_custos(
        caminho_banco
    )




    return resultado
    
    