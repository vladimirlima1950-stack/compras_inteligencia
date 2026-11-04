# compras_030_dim_calendario

# ============================================================
# CRIAÇÃO DA TABELA TB_DIM_CALENDARIO
# ============================================================

import duckdb
import pandas as pd


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    periodo = con.execute("""

        SELECT

            MIN(data_nf),
            MAX(data_nf)

        FROM tb_fato_compras

    """).fetchone()

    data_inicial = periodo[0]
    data_final = periodo[1]

    meses = pd.period_range(
        start=data_inicial,
        end=data_final,
        freq="M"
    )

    df_calendario = pd.DataFrame({

        "ano_mes":
            meses.astype(str),

        "ano":
            meses.year,

        "mes":
            meses.month

    })

    con.execute("""
        DROP TABLE IF EXISTS
        tb_dim_calendario
    """)

    con.register(
        "df_calendario",
        df_calendario
    )

    con.execute("""

        CREATE TABLE tb_dim_calendario AS

        SELECT *

        FROM df_calendario

    """)

    total = con.execute("""

        SELECT COUNT(*)

        FROM tb_dim_calendario

    """).fetchone()[0]

    print(
        f"tb_dim_calendario criada com "
        f"{total} meses."
    )

    print(df_calendario.head())

    con.close()