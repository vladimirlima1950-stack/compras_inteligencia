# compras_170_ranking_saving.py

# ============================================================
# CRIAÇÃO DA TABELA TB_RANKING_SAVING
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_ranking_saving
    """)

    con.execute("""

        CREATE TABLE tb_ranking_saving AS

        SELECT

            ROW_NUMBER() OVER (

                ORDER BY
                    saving_absoluto DESC

            ) AS ranking,

            codigo_produto,

            codigo_fornecedor,

            ultimo_mes,

            custo_atual,

            menor_custo_historico,

            fornecedor_menor_custo_historico,

            saving_absoluto,

            saving_percentual,

            status

        FROM tb_saving_potencial

        ORDER BY
            saving_absoluto DESC

    """)

    total = con.execute("""

        SELECT COUNT(*)

        FROM tb_ranking_saving

    """).fetchone()[0]

    print(
        f"tb_ranking_saving criada com "
        f"{total} oportunidades."
    )

    amostra = con.execute("""

        SELECT *

        FROM tb_ranking_saving

        LIMIT 10

    """).fetchall()

    if amostra:

        print(
            f"Maior saving encontrado: "
            f"{amostra[0]}"
        )

    con.close()