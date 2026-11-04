# compras_100_resumo_executivo.py

# ============================================================
# CRIAÇÃO DA TABELA TB_RESUMO_EXECUTIVO
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_resumo_executivo
    """)

    con.execute("""

        CREATE TABLE tb_resumo_executivo AS

        WITH resumo AS (

            SELECT

                SUM(valor_total)
                    AS valor_total_comprado,

                SUM(quantidade)
                    AS quantidade_total_comprada,

                COUNT(
                    DISTINCT codigo_produto
                ) AS produtos_distintos,

                COUNT(
                    DISTINCT codigo_fornecedor
                ) AS fornecedores_distintos

            FROM tb_fato_compras

        ),

        meses AS (

            SELECT

                COUNT(*) AS meses_periodo

            FROM tb_dim_calendario

        ),

        maior_mes AS (

            SELECT

                ano_mes,
                valor_comprado

            FROM tb_compras_mensais

            ORDER BY

                valor_comprado DESC

            LIMIT 1

        ),

        menor_mes AS (

            SELECT

                ano_mes,
                valor_comprado

            FROM tb_compras_mensais

            ORDER BY

                valor_comprado ASC

            LIMIT 1

        )

        SELECT

            r.valor_total_comprado,

            r.quantidade_total_comprada,

            r.produtos_distintos,

            r.fornecedores_distintos,

            m.meses_periodo,

            r.valor_total_comprado
            / m.meses_periodo
                AS compra_media_mensal,

            ma.ano_mes
                AS maior_mes_compra,

            ma.valor_comprado
                AS valor_maior_mes,

            me.ano_mes
                AS menor_mes_compra,

            me.valor_comprado
                AS valor_menor_mes

        FROM resumo r

        CROSS JOIN meses m

        CROSS JOIN maior_mes ma

        CROSS JOIN menor_mes me

    """)

    
    resumo = con.execute("""

    SELECT *

    FROM tb_resumo_executivo

""").fetchone()

print("\n======== RESUMO EXECUTIVO ========\n")

print(
    f"Valor Total Comprado: "
    f"{resumo[0]:,.2f}"
)

print(
    f"Quantidade Comprada: "
    f"{resumo[1]:,.2f}"
)

print(
    f"Produtos Distintos: "
    f"{resumo[2]}"
)

print(
    f"Fornecedores Distintos: "
    f"{resumo[3]}"
)

print(
    f"Meses do Período: "
    f"{resumo[4]}"
)

print(
    f"Compra Média Mensal: "
    f"{resumo[5]:,.2f}"
)

print(
    f"Maior Mês: "
    f"{resumo[6]}"
)

print(
    f"Valor do Maior Mês: "
    f"{resumo[7]:,.2f}"
)

print(
    f"Menor Mês: "
    f"{resumo[8]}"
)

print(
    f"Valor do Menor Mês: "
    f"{resumo[9]:,.2f}"
)

con.close()
    
