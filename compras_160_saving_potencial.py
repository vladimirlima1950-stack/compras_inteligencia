# compras_160_saving_potencial.py

# ============================================================
# CRIAÇÃO DA TABELA TB_SAVING_POTENCIAL
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_saving_potencial
    """)

    con.execute("""

        CREATE TABLE tb_saving_potencial AS

        WITH ultimo_preco AS (

            SELECT *

            FROM (

                SELECT

                    codigo_produto,

                    codigo_fornecedor,

                    ano_mes,

                    custo_medio,

                    ROW_NUMBER() OVER (

                        PARTITION BY

                            codigo_produto,
                            codigo_fornecedor

                        ORDER BY ano_mes DESC

                    ) AS rn

                FROM tb_produto_fornecedor_mes

            )

            WHERE rn = 1

        ),

        menor_preco AS (

            SELECT

                codigo_produto,

                codigo_fornecedor,

                MIN(custo_medio)
                    AS menor_custo_historico

            FROM tb_produto_fornecedor_mes

            GROUP BY

                codigo_produto,
                codigo_fornecedor

        )

        SELECT

            u.codigo_produto,

            u.codigo_fornecedor,

            u.ano_mes
                AS ultimo_mes,

            u.custo_medio
                AS custo_atual,

            m.menor_custo_historico,

            ROUND(

                u.custo_medio
                - m.menor_custo_historico,

                2

            ) AS saving_absoluto,

            ROUND(

                (
                    u.custo_medio
                    - m.menor_custo_historico
                )

                * 100.0

                /

                NULLIF(
                    m.menor_custo_historico,
                    0
                ),

                2

            ) AS saving_percentual

        FROM ultimo_preco u

        INNER JOIN menor_preco m

            ON u.codigo_produto =
               m.codigo_produto

           AND u.codigo_fornecedor =
               m.codigo_fornecedor

        WHERE

            u.custo_medio >
            m.menor_custo_historico

    """)

    total = con.execute("""

        SELECT COUNT(*)

        FROM tb_saving_potencial

    """).fetchone()[0]

    print(
        f"tb_saving_potencial criada com "
        f"{total} oportunidades."
    )

    amostra = con.execute("""

        SELECT *

        FROM tb_saving_potencial

        ORDER BY saving_percentual DESC

        LIMIT 10

    """).fetchall()

    if amostra:

        print(
            f"Maior oportunidade: "
            f"{amostra[0]}"
        )

    con.close()