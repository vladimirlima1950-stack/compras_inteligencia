# compras_195_indices_economicos.py

# ============================================================
# CRIAÇÃO DA TABELA TB_INDICES_ECONOMICOS_PERIODO
# ============================================================

import duckdb
import pandas as pd


# ============================================================
# CÁLCULO DE ACUMULADO
# ============================================================

def calcular_acumulado(df):

    if len(df) == 0:
        return None

    acumulado = (
        (1 + (df["valor"] / 100))
        .prod()
        - 1
    ) * 100

    return round(
        float(acumulado),
        2
    )


# ============================================================
# PROCESSAMENTO
# ============================================================

def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    print(
        "\n======== ÍNDICES ECONÔMICOS DO PERÍODO ========\n"
    )

    # --------------------------------------------------------
    # PERÍODO DE ANÁLISE
    # --------------------------------------------------------

    periodo = con.execute("""

        SELECT

            data_inicio,
            data_fim

        FROM tb_periodo_analise

    """).fetchone()

    data_inicio = periodo[0]
    data_fim = periodo[1]

    print(
        f"Período analisado: "
        f"{data_inicio} até {data_fim}"
    )

    # --------------------------------------------------------
    # CARREGA ÍNDICES
    # --------------------------------------------------------

    df = con.execute("""

        SELECT

            data_referencia,
            indice,
            valor

        FROM tb_indices_economicos

        WHERE data_referencia
        BETWEEN ? AND ?

        ORDER BY
            indice,
            data_referencia

    """, (
        data_inicio,
        data_fim
    )).fetchdf()

    # --------------------------------------------------------
    # CÁLCULO DOS ACUMULADOS
    # --------------------------------------------------------

    acumulados = []

    for indice in [
        "IPCA",
        "IGPM",
        "IPAM",
        "IPADI"
    ]:

        df_indice = df[
            df["indice"] == indice
        ]

        acumulado = calcular_acumulado(
            df_indice
        )

        acumulados.append(
            (
                indice,
                acumulado
            )
        )

    # --------------------------------------------------------
    # TABELA FINAL
    # --------------------------------------------------------

    con.execute("""

        DROP TABLE IF EXISTS
        tb_indices_economicos_periodo

    """)

    con.execute("""

        CREATE TABLE
        tb_indices_economicos_periodo (

            indice VARCHAR,
            acumulado DOUBLE

        )

    """)

    con.executemany("""

        INSERT INTO
        tb_indices_economicos_periodo

        VALUES (?, ?)

    """, acumulados)

    print(
        "\nÍndices acumulados:"
    )

    for item in acumulados:

        print(
            f"{item[0]}: "
            f"{item[1]}%"
        )

    total = con.execute("""

        SELECT COUNT(*)

        FROM tb_indices_economicos_periodo

    """).fetchone()[0]

    print(
        f"\ntb_indices_economicos_periodo criada com "
        f"{total} registros."
    )

    con.close()


# ============================================================
# TESTE LOCAL
# ============================================================

if __name__ == "__main__":

    run(
        "compras_inteligencia.duckdb"
    )