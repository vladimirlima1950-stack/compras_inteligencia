# Compras_080_historico_compras.py

# ============================================================
# HISTORICO DE COMPRAS
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_historico_compras
    """)

    con.execute("""
        CREATE TABLE tb_historico_compras AS

        SELECT

            codigo_produto,

            data_nf AS data_compra,

            codigo_fornecedor,

            custo_unitario,

            quantidade,

            valor_total AS custo_total

        FROM tb_fato_compras

        ORDER BY
            codigo_produto,
            data_nf
    """)

    total = con.execute("""
        SELECT COUNT(*)
        FROM tb_historico_compras
    """).fetchone()[0]

    print(
        f"tb_historico_compras criada com "
        f"{total} registros."
    )

    amostra = con.execute("""
        SELECT *
        FROM tb_historico_compras
        LIMIT 5
    """).fetchall()

    print("\nAmostra:")

    for linha in amostra:
        print(linha)

    con.close()


if __name__ == "__main__":

    caminho_banco = (
        "compras_inteligencia.duckdb"
    )

    run(caminho_banco)