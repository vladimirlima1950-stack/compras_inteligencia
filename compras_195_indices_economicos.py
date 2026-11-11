# compras_195_indices_economicos.py

# ============================================================
# CRIAÇÃO DAS TABELAS
# TB_INDICES_ECONOMICOS
# TB_INDICES_ECONOMICOS_PERIODO
# ============================================================

import duckdb
import pandas as pd

from bcb import sgs


# ============================================================
# CALCULA ACUMULADO
# ============================================================

def calcular_acumulado(serie):

    serie = serie.dropna()

    if len(serie) == 0:
        return None

    acumulado = (
        (1 + serie / 100)
        .prod()
        - 1
    ) * 100

    return round(
        acumulado,
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
        "\n======== ÍNDICES ECONÔMICOS ========\n"
    )

    # --------------------------------------------------------
    # PERÍODO DO CLIENTE
    # --------------------------------------------------------

    periodo = con.execute("""

        SELECT
            MIN(data_nf),
            MAX(data_nf)

        FROM tb_fato_compras

    """).fetchone()

    data_inicial = periodo[0]
    data_final = periodo[1]

    print(
        f"Período analisado: "
        f"{data_inicial} até {data_final}"
    )

    # --------------------------------------------------------
    # DOWNLOAD DOS ÍNDICES
    # --------------------------------------------------------

    series_dict = {
        "IPCA": 433,
        "IGPM": 189,
        "IPAM": 7450,
        "IPADI": 190
    }

    try:

        df = sgs.get(
            series_dict,
            start=data_inicial,
            end=data_final
        )

    except Exception as erro:

        print(
            f"Erro ao acessar "
            f"Banco Central: {erro}"
        )

        con.close()
        return

    # --------------------------------------------------------
    # TB_INDICES_ECONOMICOS
    # --------------------------------------------------------

    con.execute("""

        DROP TABLE IF EXISTS
        tb_indices_economicos

    """)

    con.execute("""

        CREATE TABLE
        tb_indices_economicos (

            data_referencia DATE,
            indice VARCHAR,
            valor DOUBLE

        )

    """)

    registros = []

    for indice in df.columns:

        df_temp = (
            df[[indice]]
            .dropna()
            .reset_index()
        )

        for _, row in df_temp.iterrows():

            registros.append(

                (
                    row["Date"],
                    indice,
                    float(row[indice])
                )

            )

    con.executemany("""

        INSERT INTO
        tb_indices_economicos

        VALUES (?, ?, ?)

    """, registros)

    print(
        f"tb_indices_economicos criada com "
        f"{len(registros)} registros."
    )

    # --------------------------------------------------------
    # ACUMULADOS
    # --------------------------------------------------------

    acumulados = []

    for indice in df.columns:

        valor = calcular_acumulado(
            df[indice]
        )

        acumulados.append(
            (
                indice,
                valor
            )
        )

    # --------------------------------------------------------
    # TB_INDICES_ECONOMICOS_PERIODO
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

    for indice, valor in acumulados:

        print(
            f"{indice}: "
            f"{valor}%"
        )

    amostra = con.execute("""

        SELECT *

        FROM tb_indices_economicos_periodo

    """).fetchall()

    print(
        "\nTabela criada:"
    )

    print(
        amostra
    )

    con.close()