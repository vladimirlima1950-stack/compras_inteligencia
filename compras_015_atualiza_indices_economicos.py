
# compras_015_atualiza_indices_economicos.py
# ============================================================
# ATUALIZA BASE DE ÍNDICES ECONÔMICOS
# ============================================================

import duckdb
import pandas as pd

from bcb import sgs


def run(caminho_banco):

    print(
        "\n======== ATUALIZAÇÃO DOS ÍNDICES ECONÔMICOS ========\n"
    )

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    series_dict = {
        "IPCA": 433,
        "IGPM": 189,
        "IPAM": 7450,
        "IPADI": 190
    }

    try:

        df = sgs.get(
            series_dict,
            start="2025-01-01"
        )

    except Exception as erro:

        print(
            f"Erro ao acessar Banco Central: "
            f"{erro}"
        )

        con.close()
        return

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

        df_indice = (
            df[[indice]]
            .dropna()
            .reset_index()
        )

        for _, row in df_indice.iterrows():

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

    total = con.execute("""

        SELECT COUNT(*)

        FROM tb_indices_economicos

    """).fetchone()[0]

    print(
        f"tb_indices_economicos criada com "
        f"{total} registros."
    )

    resumo = con.execute("""

        SELECT
            indice,
            COUNT(*) registros,
            MIN(data_referencia),
            MAX(data_referencia)

        FROM tb_indices_economicos

        GROUP BY indice

        ORDER BY indice

    """).fetchall()

    print("\nResumo dos índices:\n")

    for item in resumo:

        print(
            f"{item[0]} | "
            f"{item[1]} registros | "
            f"{item[2]} até {item[3]}"
        )

    con.close()
        



# ============================================================
# TESTE LOCAL
# ============================================================

if __name__ == "__main__":

    print("INICIANDO TESTE...")

    run(
        "compras_inteligencia.duckdb"
    )

    print("FINALIZADO.")
