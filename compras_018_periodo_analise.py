# compras_018_periodo_analise.py

# ============================================================
# CRIAÇÃO DA TABELA TB_PERIODO_ANALISE
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_periodo_analise
    """)

    con.execute("""

        CREATE TABLE tb_periodo_analise AS

        WITH referencia AS (

            SELECT

                MAX(data_nf)
                    AS maior_data_cliente

            FROM tb_compras_validada

        ),

        periodo AS (

            SELECT

                DATE_TRUNC(
                    'month',
                    maior_data_cliente
                ) - INTERVAL '1 month'
                    AS data_fim

            FROM referencia

        )

        SELECT

            data_fim,

            DATE_TRUNC(
                'month',
                data_fim - INTERVAL '23 month'
            ) AS data_inicio,

            24 AS meses_analisados

        FROM periodo

    """)

    periodo = con.execute("""

        SELECT

            data_inicio,
            data_fim,
            meses_analisados

        FROM tb_periodo_analise

    """).fetchone()

    print(
        "\n======== PERÍODO DE ANÁLISE ========\n"
    )

    print(
        f"Data Inicial: "
        f"{periodo[0]}"
    )

    print(
        f"Data Final: "
        f"{periodo[1]}"
    )

    print(
        f"Meses Analisados: "
        f"{periodo[2]}"
    )

    con.close()


# ============================================================
# TESTE LOCAL
# ============================================================

if __name__ == "__main__":

    run(
        "compras_inteligencia.duckdb"
    )