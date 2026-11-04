# compras_130_ranking_produto.py

# ============================================================
# CRIAÇÃO DA TABELA TB_RANKING_PRODUTOS
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_ranking_produtos
    """)

    con.execute("""

        CREATE TABLE tb_ranking_produtos AS

        WITH compras_produto AS (

            SELECT

                codigo_produto,

                SUM(valor_total)
                    AS valor_comprado

            FROM tb_fato_compras

            GROUP BY codigo_produto

        ),

        total_compras AS (

            SELECT

                SUM(valor_comprado)
                    AS valor_total

            FROM compras_produto

        )

        SELECT

            ROW_NUMBER() OVER (

                ORDER BY valor_comprado DESC

            ) AS ranking,

            codigo_produto,

            valor_comprado,

            ROUND(

                valor_comprado
                * 100.0
                / total_compras.valor_total,

                2

            ) AS percentual

        FROM compras_produto

        CROSS JOIN total_compras

        ORDER BY valor_comprado DESC

    """)

    total = con.execute("""

        SELECT COUNT(*)

        FROM tb_ranking_produtos

    """).fetchone()[0]

    print(
        f"tb_ranking_produtos criada com "
        f"{total} produtos."
    )

    amostra = con.execute("""

        SELECT *

        FROM tb_ranking_produtos

        LIMIT 10

    """).fetchall()

    print(amostra)

    con.close()