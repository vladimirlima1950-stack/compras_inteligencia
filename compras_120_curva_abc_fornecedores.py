# compras_120_curva_abc_fornecedores.py

# ============================================================
# CRIAÇÃO DA TABELA TB_CURVA_ABC_FORNECEDORES
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_curva_abc_fornecedores
    """)

    con.execute("""

        CREATE TABLE tb_curva_abc_fornecedores AS

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

            FROM tb_ranking_fornecedores

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

        FROM tb_curva_abc_fornecedores

    """).fetchone()[0]

    print(
        f"tb_curva_abc_fornecedores criada com "
        f"{total} fornecedores."
    )

    amostra = con.execute("""

        SELECT *

        FROM tb_curva_abc_fornecedores

        LIMIT 10

    """).fetchall()

    print(
    
        f"Primeiro fornecedor ABC: "
        f"{amostra[0]}"
    )

    con.close()