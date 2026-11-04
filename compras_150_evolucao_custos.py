# compras_150_evolucao_custos.py

# ============================================================
# CRIAÇÃO DA TABELA TB_EVOLUCAO_CUSTOS
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_evolucao_custos
    """)

    con.execute("""

        CREATE TABLE tb_evolucao_custos AS

        SELECT

            codigo_produto,

            codigo_fornecedor,

            ano_mes,

            custo_medio,

            LAG(custo_medio) OVER (

                PARTITION BY

                    codigo_produto,
                    codigo_fornecedor

                ORDER BY ano_mes

            ) AS custo_mes_anterior,

            ROUND(

                (
                    custo_medio
                    -
                    LAG(custo_medio) OVER (

                        PARTITION BY

                            codigo_produto,
                            codigo_fornecedor

                        ORDER BY ano_mes

                    )
                )

                * 100.0

                /

                NULLIF(

                    LAG(custo_medio) OVER (

                        PARTITION BY

                            codigo_produto,
                            codigo_fornecedor

                        ORDER BY ano_mes

                    ),

                    0

                ),

                2

            ) AS variacao_percentual

        FROM tb_produto_fornecedor_mes

    """)

    total = con.execute("""

        SELECT COUNT(*)

        FROM tb_evolucao_custos

    """).fetchone()[0]

    print(
        f"tb_evolucao_custos criada com "
        f"{total} registros."
    )

    amostra = con.execute("""

        SELECT *

        FROM tb_evolucao_custos

        WHERE custo_mes_anterior IS NOT NULL

        LIMIT 10

    """).fetchall()

    if amostra:

        print(
            f"Primeira evolução encontrada: "
            f"{amostra[0]}"
        )

    con.close()