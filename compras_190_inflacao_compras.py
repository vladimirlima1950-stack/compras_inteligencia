# compras_190_inflacao_compras.py

# ============================================================
# CRIAÇÃO DA TABELA TB_INFLACAO_COMPRAS
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_inflacao_compras
    """)

    con.execute("""

        CREATE TABLE tb_inflacao_compras AS

        SELECT

            ano_mes,

            COUNT(*) AS itens_avaliados,

            SUM(

                CASE

                    WHEN variacao_percentual > 0

                    THEN 1

                    ELSE 0

                END

            ) AS itens_com_aumento,

            SUM(

                CASE

                    WHEN variacao_percentual < 0

                    THEN 1

                    ELSE 0

                END

            ) AS itens_com_reducao,

            ROUND(

                AVG(
                    variacao_percentual
                ),

                2

            ) AS inflacao_media

        FROM tb_evolucao_custos

        WHERE variacao_percentual IS NOT NULL

        GROUP BY

            ano_mes

        ORDER BY

            ano_mes

    """)

    total = con.execute("""

        SELECT COUNT(*)

        FROM tb_inflacao_compras

    """).fetchone()[0]

    print(
        f"tb_inflacao_compras criada com "
        f"{total} meses."
    )

    amostra = con.execute("""

        SELECT *

        FROM tb_inflacao_compras

        ORDER BY ano_mes

        LIMIT 10

    """).fetchall()

    if amostra:

        print(
            f"Primeiro mês avaliado: "
            f"{amostra[0]}"
        )

    resumo = con.execute("""

        SELECT

            ROUND(
                AVG(inflacao_media),
                2
            )

        FROM tb_inflacao_compras

    """).fetchone()

    print(
       f"Inflação média do período: "
       f"{resumo[0]}%"
    )

    con.close()