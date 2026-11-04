# compras_110_ranking_fornecedores.py
# ============================================================
# CRIAÇÃO DA TABELA TB_RANKING_FORNECEDORES
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_ranking_fornecedores
    """)

    con.execute("""

        CREATE TABLE tb_ranking_fornecedores AS

        WITH compras_fornecedor AS (

            SELECT

                codigo_fornecedor,

                SUM(valor_total)
                    AS valor_comprado

            FROM tb_fato_compras

            GROUP BY codigo_fornecedor

        ),

        total_compras AS (

            SELECT

                SUM(valor_comprado)
                    AS valor_total

            FROM compras_fornecedor

        )

        SELECT

            ROW_NUMBER() OVER (

                ORDER BY
                    valor_comprado DESC

            ) AS ranking,

            codigo_fornecedor,

            valor_comprado,

            ROUND(

                valor_comprado
                * 100.0
                / total_compras.valor_total,

                2

            ) AS percentual

        FROM compras_fornecedor

        CROSS JOIN total_compras

        ORDER BY valor_comprado DESC

    """)

    total = con.execute("""

        SELECT COUNT(*)

        FROM tb_ranking_fornecedores

    """).fetchone()[0]

    print(
        f"tb_ranking_fornecedores criada com "
        f"{total} fornecedores."
    )

    amostra = con.execute("""

        SELECT *

        FROM tb_ranking_fornecedores

        LIMIT 10

    """).fetchall()

    print(amostra)

    con.close()