# compras_050_produto_mes

# ============================================================
# CRIAÇÃO DA TABELA TB_PRODUTO_MES
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_produto_mes
    """)

    con.execute("""

        CREATE TABLE tb_produto_mes AS

        SELECT

            codigo_produto,

            ano_mes,

            SUM(quantidade)
                AS quantidade_comprada,

            SUM(valor_total)
                AS valor_comprado,

            AVG(custo_unitario)
                AS custo_medio,

            COUNT(
                DISTINCT codigo_fornecedor
            ) AS fornecedores

        FROM tb_fato_compras

        GROUP BY

            codigo_produto,
            ano_mes

    """)

    total = con.execute("""

        SELECT COUNT(*)

        FROM tb_produto_mes

    """).fetchone()[0]

    print(
        f"tb_produto_mes criada com "
        f"{total} registros."
    )

    amostra = con.execute("""

        SELECT *

        FROM tb_produto_mes

        LIMIT 10

    """).fetchall()

    print(amostra)

    con.close()