# compras_020_fato_compras.py

import duckdb


# ============================================================
# CRIAÇÃO DA TABELA FATO_COMPRAS
# ============================================================

def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    # --------------------------------------------------------
    # Remove tabela anterior (se existir)
    # --------------------------------------------------------

    con.execute("""
        DROP TABLE IF EXISTS tb_fato_compras
    """)

    # --------------------------------------------------------
    # Cria tabela fato_compras
    # --------------------------------------------------------

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
            )
                AS ano_mes

        FROM tb_compras_validada
    """)

    total_registros = con.execute("""
        SELECT COUNT(*)
        FROM tb_fato_compras
    """).fetchone()[0]

    print(
        f"tb_fato_compras criada ({total_registros} registros)"
    )

    con.close()