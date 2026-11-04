# compras_140_curva_abc_produtos.py

# ============================================================
# CRIAÇÃO DA TABELA TB_CURVA_ABC_PRODUTOS
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_curva_abc_produtos
    """)

    con.execute("""

        CREATE TABLE tb_curva_abc_produtos AS

        WITH base AS (

            SELECT

                *,

                SUM(percentual)
                OVER (

                    ORDER BY ranking

                    ROWS BETWEEN
                    UNBOUNDED PRECEDING
                    AND CURRENT ROW

                ) AS percentual_acumulado

            FROM tb_ranking_produtos

        )

        SELECT

            *,

            CASE

                WHEN percentual_acumulado <= 80
                THEN 'A'

                WHEN percentual_acumulado <= 95
                THEN 'B'

                ELSE 'C'

            END AS classe

        FROM base

    """)

    total = con.execute("""

        SELECT COUNT(*)

        FROM tb_curva_abc_produtos

    """).fetchone()[0]

    print(
        f"tb_curva_abc_produtos criada com "
        f"{total} produtos."
    )

    amostra = con.execute("""

        SELECT *

        FROM tb_curva_abc_produtos

        LIMIT 10

    """).fetchall()

    print(
        f"Primeiro produto ABC: "
        f"{amostra[0]}"
    )

    con.close()