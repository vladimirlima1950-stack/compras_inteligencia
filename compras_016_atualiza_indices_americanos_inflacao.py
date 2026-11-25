# ============================================================
# ATUALIZA PLANILHA DE ÍNDICES ECONÔMICOS (EUA - FRED)
# ============================================================

from io import StringIO
from pathlib import Path
from urllib.request import urlopen

import pandas as pd


# ============================================================
# CONFIGURAÇÕES
# ============================================================

ARQUIVO_INDICES = "dados/indices_economicos_us.xlsx"
ABA_INDICES = "tb_indices_economicos"
ABA_PARAMETROS = "parametros"

SERIES_FRED = {
    "CPI_US": "CPIAUCSL",       # Equivalente geral ao IPCA (CPI-U)
    "PPI_GOODS": "WPSFD49207",  # PPI Finished Goods
    "PPI_COMMODITIES": "PPIACO",  # PPI All Commodities
    "PPI_INTERMEDIATE": "WPSID61"  # PPI Processed Goods for Intermediate Demand
}


def baixar_serie_fred(codigo_serie: str, data_inicio: str) -> pd.Series:
    """Baixa a série mensal do FRED via CSV e retorna variação % mensal."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={codigo_serie}"
    with urlopen(url, timeout=30) as resp:
        csv_texto = resp.read().decode("utf-8")

    df = pd.read_csv(StringIO(csv_texto))
    # O FRED usa 'observation_date' ou 'DATE' dependendo da exportação
    col_data = "observation_date" if "observation_date" in df.columns else df.columns[0]
    col_valor = codigo_serie if codigo_serie in df.columns else df.columns[1]

    df[col_data] = pd.to_datetime(df[col_data], errors="coerce")
    df[col_valor] = pd.to_numeric(df[col_valor], errors="coerce")
    df = df.dropna(subset=[col_data, col_valor]).sort_values(col_data)

    # Calcula variação mensal (%) e filtra a partir de data_inicio
    df["variacao_mensal_pct"] = df[col_valor].pct_change() * 100
    df_filtrado = df[df[col_data] >= pd.to_datetime(data_inicio)].dropna(subset=["variacao_mensal_pct"])

    return df_filtrado.set_index(col_data)["variacao_mensal_pct"]


def run():
    print("\n======== ATUALIZAÇÃO DOS ÍNDICES ECONÔMICOS (EUA) ========\n")

    arquivo = Path(ARQUIVO_INDICES)
    if not arquivo.exists():
        print("Planilha não encontrada.")
        return

    df_atual = pd.read_excel(ARQUIVO_INDICES, sheet_name=ABA_INDICES)
    
    
    df_atual["data_referencia"] = pd.to_datetime(
        df_atual["data_referencia"],
        errors="coerce"
    )

    ultima_data = df_atual["data_referencia"].max()
    print(f"Última data encontrada: {ultima_data.date() if pd.notna(ultima_data) else 'Nenhuma (base vazia)'}")

    if pd.isna(ultima_data):
        # Primeira carga quando a tabela ainda não tem datas válidas
        data_inicio = "2024-01-01"
        data_busca = (pd.to_datetime(data_inicio) - pd.DateOffset(months=1)).strftime("%Y-%m-%d")
    else:
        data_busca = ultima_data.strftime("%Y-%m-%d")
        data_inicio = (ultima_data + pd.DateOffset(months=1)).strftime("%Y-%m-%d")

    print(f"Buscando dados a partir de: {data_inicio}")
    
    if pd.isna(ultima_data):
        # Primeira carga quando a tabela ainda não tem datas válidas
        data_inicio = "2024-01-01"
        data_busca = (
            pd.to_datetime(data_inicio) - pd.DateOffset(months=1)
        ).strftime("%Y-%m-%d")
    else:
        data_busca = ultima_data.strftime("%Y-%m-%d")
        data_inicio = (
            ultima_data + pd.DateOffset(months=1)
        ).strftime("%Y-%m-%d")

    print(f"Buscando dados a partir de: {data_inicio}")
    
    
    registros = []

    for nome_indice, codigo_fred in SERIES_FRED.items():
        try:
            serie = baixar_serie_fred(codigo_fred, data_busca)
            serie = serie[serie.index >= pd.to_datetime(data_inicio)]

            for dt, val in serie.items():
                registros.append({
                    "data_referencia": dt,
                    "indice": nome_indice,
                    "valor": float(val)
                })
        except Exception as erro:
            print(f"Erro ao obter {nome_indice} ({codigo_fred}): {erro}")

    if not registros:
        print("Nenhum índice novo encontrado.")
        return

    df_novo = pd.DataFrame(registros)

    df_final = pd.concat([df_atual, df_novo], ignore_index=True)
    df_final = df_final.drop_duplicates(
        subset=["data_referencia", "indice"],
        keep="last"
    ).sort_values(["indice", "data_referencia"]).reset_index(drop=True)

    duplicados = df_final.duplicated(subset=["data_referencia", "indice"]).sum()
    print(f"Duplicados encontrados: {duplicados}")

    parametros = pd.DataFrame([
        {"parametro": "meses_analise", "valor": 24},
        {"parametro": "versao_base", "valor": 1},
        {"parametro": "data_atualizacao", "valor": pd.Timestamp.today().date()}
    ])

    with pd.ExcelWriter(ARQUIVO_INDICES, engine="openpyxl") as writer:
        df_final.to_excel(writer, sheet_name=ABA_INDICES, index=False)
        parametros.to_excel(writer, sheet_name=ABA_PARAMETROS, index=False)

    print(f"Base atualizada com {len(df_final)} registros.")
    print("Atualização concluída.")


if __name__ == "__main__":
    run()