# compras_195_indices_economicos.py



# ============================================================
# CRIAÇÃO DA TABELA TB_INDICES_ECONOMICOS_PERIODO
# ============================================================

import duckdb
import pandas as pd


# ============================================================
# CALCULA ACUMULADO
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

    print(
            "\n======== EXECUTANDO MODULO 195 ==========\n"
        )


    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    print(
        "\n======== ÍNDICES ECONÔMICOS DO PERÍODO ========\n"
    )

    # --------------------------------------------------------
    # OBTÉM PERÍODO DAS COMPRAS
    # --------------------------------------------------------

    periodo = con.execute("""

        SELECT

            MIN(data_nf),
            MAX(data_nf)

        FROM tb_fato_compras

    """).fetchone()

    data_inicio = periodo[0]
    data_fim = periodo[1]

    print(
        f"Período analisado: "
        f"{data_inicio} até {data_fim}"
    )

    # --------------------------------------------------------
    # CARREGA PLANILHA DE ÍNDICES
    # --------------------------------------------------------

    df_indices = pd.read_excel(
        "dados/indices_economicos.xlsx",
        sheet_name="tb_indices_economicos"
    )

    # garante tipo data
    df_indices["data_referencia"] = pd.to_datetime(
        df_indices["data_referencia"]
    )

    # --------------------------------------------------------
    # FILTRA PERÍODO
    # --------------------------------------------------------

    df_indices = df_indices[

        (
            df_indices["data_referencia"]
            >= pd.to_datetime(data_inicio)
        )

        &

        (
            df_indices["data_referencia"]
            <= pd.to_datetime(data_fim)
        )

    ]

    print(
        f"Registros encontrados: "
        f"{len(df_indices)}"
    )

    # --------------------------------------------------------
    # CALCULA ACUMULADOS
    # --------------------------------------------------------

    acumulados = []

    for indice in [

        "IPCA",
        "IGPM",
        "IPAM",
        "IPADI"

    ]:

        df_indice = df_indices[
            df_indices["indice"] == indice
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
    # CRIA TABELA FINAL
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

    # --------------------------------------------------------
    # LOG
    # --------------------------------------------------------

    print(
        "\nÍndices acumulados:"
    )

    for indice, valor in acumulados:

        print(
            f"{indice}: {valor}%"
        )

    total = con.execute("""

        SELECT COUNT(*)

        FROM tb_indices_economicos_periodo

    """).fetchone()[0]

    print(

        f"\ntb_indices_economicos_periodo "
        f"criada com {total} registros."

    )

    con.close()


# ============================================================
# TESTE LOCAL
# ============================================================

if __name__ == "__main__":

    run(
        "compras_inteligencia.duckdb"
    )