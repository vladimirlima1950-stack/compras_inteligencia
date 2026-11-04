# compras_060_fornecedor_mes.py

# ============================================================
# CRIAÇÃO DA TABELA TB_FORNECEDOR_MES
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_fornecedor_mes
    """)

    con.execute("""

        CREATE TABLE tb_fornecedor_mes AS

        SELECT

            codigo_fornecedor,

            ano_mes,

            SUM(quantidade)
                AS quantidade_comprada,

            SUM(valor_total)
                AS valor_comprado,

            AVG(custo_unitario)
                AS custo_medio,

            COUNT(
                DISTINCT codigo_produto
            ) AS produtos

        FROM tb_fato_compras

        GROUP BY

            codigo_fornecedor,
            ano_mes

    """)

    total = con.execute("""

        SELECT COUNT(*)

        FROM tb_fornecedor_mes

    """).fetchone()[0]

    print(
        f"tb_fornecedor_mes criada com "
        f"{total} registros."
    )

    amostra = con.execute("""

        SELECT *

        FROM tb_fornecedor_mes

        LIMIT 10

    """).fetchall()

    print(amostra)

    con.close()