# ============================================================
# CRIAÇÃO DA TABELA TB_FATO_COMPRAS
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_fato_compras
    """)

    con.execute("""
        CREATE TABLE tb_fato_compras AS

        SELECT

            codigo_produto,

            codigo_fornecedor,

            data_nf,

            quantidade,

            custo_unitario,

            quantidade * custo_unitario
                AS valor_total,

            YEAR(data_nf)
                AS ano,

            MONTH(data_nf)
                AS mes,

            STRFTIME(
                data_nf,
                '%Y-%m'
            ) AS ano_mes

        FROM tb_compras_validada
    """)

    total = con.execute("""
        SELECT COUNT(*)
        FROM tb_fato_compras
    """).fetchone()[0]


periodo = con.execute("""

    SELECT

        MIN(data_nf),
        MAX(data_nf)

    FROM tb_fato_compras

""").fetchone()

print(
    f"Período encontrado: "
    f"{periodo[0]} até {periodo[1]}"
)


amostra = con.execute("""

    SELECT

        codigo_produto,
        quantidade,
        custo_unitario,
        valor_total,
        ano_mes

    FROM tb_fato_compras

    LIMIT 5

""").fetchall()

print(amostra)

    print(
        f"tb_fato_compras criada com {total} registros."
    )

    con.close()