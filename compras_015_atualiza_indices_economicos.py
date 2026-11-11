# compras_015_atualiza_indices_economicos.py

# ============================================================
# ATUALIZA PLANILHA DE ÍNDICES ECONÔMICOS
# ============================================================

from pathlib import Path

import pandas as pd

from bcb import sgs


# ============================================================
# CONFIGURAÇÕES
# ============================================================

ARQUIVO_INDICES = (
    "dados/indices_economicos.xlsx"
)

ABA_INDICES = (
    "tb_indices_economicos"
)

ABA_PARAMETROS = (
    "parametros"
)


# ============================================================
# PROCESSAMENTO
# ============================================================

def run():

    print(
        "\n======== ATUALIZAÇÃO DOS ÍNDICES ECONÔMICOS ========\n"
    )

    arquivo = Path(
        ARQUIVO_INDICES
    )

    if not arquivo.exists():

        print(
            "Planilha não encontrada."
        )

        return

    # --------------------------------------------------------
    # LEITURA DA BASE EXISTENTE
    # --------------------------------------------------------

    df_atual = pd.read_excel(
        ARQUIVO_INDICES,
        sheet_name=ABA_INDICES
    )

    df_atual["data_referencia"] = pd.to_datetime(
        df_atual["data_referencia"]
    )

    ultima_data = (
        df_atual["data_referencia"]
        .max()
    )

    print(
        f"Última data encontrada: "
        f"{ultima_data.date()}"
    )

    data_inicio = (
        ultima_data +
        pd.DateOffset(months=1)
    ).strftime(
        "%Y-%m-%d"
    )

    print(
        f"Buscando dados a partir de: "
        f"{data_inicio}"
    )

    # --------------------------------------------------------
    # SÉRIES SGS
    # --------------------------------------------------------

    series_dict = {
        "IPCA": 433,
        "IGPM": 189,
        "IPAM": 7450,
        "IPADI": 190
    }

    try:

        df_sgs = sgs.get(
            series_dict,
            start=data_inicio
        )

    except Exception as erro:

        print(
            f"Erro ao acessar Banco Central: "
            f"{erro}"
        )

        return

    # --------------------------------------------------------
    # SEM NOVOS DADOS
    # --------------------------------------------------------

    if df_sgs.empty:

        print(
            "Nenhum mês novo encontrado."
        )

        return

    # --------------------------------------------------------
    # TRANSFORMA PARA FORMATO PADRÃO
    # --------------------------------------------------------

    registros = []

    for indice in df_sgs.columns:

        df_indice = (
            df_sgs[[indice]]
            .dropna()
            .reset_index()
        )

        for _, row in df_indice.iterrows():

            registros.append(
                {
                    "data_referencia":
                        row["Date"],

                    "indice":
                        indice,

                    "valor":
                        float(
                            row[indice]
                        )
                }
            )

    df_novo = pd.DataFrame(
        registros
    )

    # --------------------------------------------------------
    # CONCATENA BASE ANTIGA + NOVA
    # --------------------------------------------------------

    df_final = pd.concat(
        [
            df_atual,
            df_novo
        ],
        ignore_index=True
    )

    # --------------------------------------------------------
    # REMOVE DUPLICADOS
    # CHAVE:
    # data_referencia + indice
    # --------------------------------------------------------

    df_final = df_final.drop_duplicates(
        subset=[
            "data_referencia",
            "indice"
        ],
        keep="last"
    )

    # --------------------------------------------------------
    # ORDENA
    # --------------------------------------------------------

    df_final = df_final.sort_values(
        [
            "indice",
            "data_referencia"
        ]
    )

    df_final = df_final.reset_index(
        drop=True
    )

    # --------------------------------------------------------
    # VALIDAÇÃO
    # --------------------------------------------------------

    duplicados = (
        df_final
        .duplicated(
            subset=[
                "data_referencia",
                "indice"
            ]
        )
        .sum()
    )

    print(
        f"Duplicados encontrados: "
        f"{duplicados}"
    )

    # --------------------------------------------------------
    # PARAMETROS
    # --------------------------------------------------------

    parametros = pd.DataFrame(
        [
            {
                "parametro":
                    "meses_analise",

                "valor":
                    24
            },
            {
                "parametro":
                    "versao_base",

                "valor":
                    1
            },
            {
                "parametro":
                    "data_atualizacao",

                "valor":
                    pd.Timestamp.today()
                    .date()
            }
        ]
    )

    # --------------------------------------------------------
    # SALVA
    # --------------------------------------------------------

    with pd.ExcelWriter(
        ARQUIVO_INDICES,
        engine="openpyxl"
    ) as writer:

        df_final.to_excel(
            writer,
            sheet_name=ABA_INDICES,
            index=False
        )

        parametros.to_excel(
            writer,
            sheet_name=ABA_PARAMETROS,
            index=False
        )

    print(
        f"Base atualizada com "
        f"{len(df_final)} registros."
    )

    print(
        "Atualização concluída."
    )


# ============================================================
# TESTE LOCAL
# ============================================================

if __name__ == "__main__":

    run()