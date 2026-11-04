# compras_040_compras_mensais
# ============================================================
# CRIAÇÃO DA TABELA TB_COMPRAS_MENSAIS
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_compras_mensais
    """)

    con.execute("""

        CREATE TABLE tb_compras_mensais AS

        WITH compras AS (

            SELECT

                ano_mes,

                SUM(valor_total)
                    AS valor_comprado,

                SUM(quantidade)
                    AS quantidade_comprada,

                COUNT(
                    DISTINCT codigo_fornecedor
                ) AS fornecedores,

                COUNT(
                    DISTINCT codigo_produto
                ) AS produtos,

                COUNT(*)
                    AS registros

            FROM tb_fato_compras

            GROUP BY ano_mes
        )

        SELECT

            c.ano_mes,

            c.ano,

            c.mes,

            COALESCE(
                m.valor_comprado,
                0
            ) AS valor_comprado,

            COALESCE(
                m.quantidade_comprada,
                0
            ) AS quantidade_comprada,

            COALESCE(
                m.fornecedores,
                0
            ) AS fornecedores,

            COALESCE(
                m.produtos,
                0
            ) AS produtos,

            COALESCE(
                m.registros,
                0
            ) AS registros

        FROM tb_dim_calendario c

        LEFT JOIN compras m

            ON c.ano_mes = m.ano_mes

        ORDER BY c.ano_mes

    """)

    total = con.execute("""

        SELECT COUNT(*)

        FROM tb_compras_mensais

    """).fetchone()[0]

    print(
        f"tb_compras_mensais criada com "
        f"{total} meses."
    )

    amostra = con.execute("""

        SELECT *

        FROM tb_compras_mensais

        LIMIT 5

    """).fetchall()

    print(amostra)

    con.close()