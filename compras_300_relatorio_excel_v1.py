# compras_300_relatorio_excel.py

# ============================================================
# GERAÇÃO DO RELATÓRIO EXCEL
# ============================================================

import duckdb
import pandas as pd


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    arquivo_saida = (
        "compras_inteligencia_relatorio.xlsx"
    )

    abas = {

        "Resumo Executivo":
        "tb_relatorio_executivo",

        "Compras Mensais":
        "tb_compras_mensais",

        "Ranking Fornec":
        "tb_ranking_fornecedores",

        "ABC Fornec":
        "tb_curva_abc_fornecedores",

        "Ranking Produtos":
        "tb_ranking_produtos",

        "ABC Produtos":
        "tb_curva_abc_produtos",

        "Saving":
        "tb_ranking_saving",

        "Inflacao":
        "tb_inflacao_compras"

    }

    with pd.ExcelWriter(
        arquivo_saida,
        engine="openpyxl"
    ) as writer:

        for aba, tabela in abas.items():

            try:

                df = con.execute(
                    f"""
                    SELECT *
                    FROM {tabela}
                    """
                ).df()

                df.to_excel(
                    writer,
                    sheet_name=aba,
                    index=False
                )

                print(
                    f"Aba criada: {aba}"
                )

            except Exception as e:

                print(
                    f"Erro na tabela "
                    f"{tabela}: {e}"
                )

    con.close()

    print(
        f"Relatório criado: "
        f"{arquivo_saida}"
    )

    return arquivo_saida