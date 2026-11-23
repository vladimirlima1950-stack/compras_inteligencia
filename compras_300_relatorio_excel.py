# compras_300_relatorio_excel.py

# ============================================================
# COMPRAS INTELIGENCIA
# RELATÓRIO EXCEL V2
# ============================================================

import duckdb
import pandas as pd

# ============================================================
# EVOLUÇÃO HISTÓRICA
# ============================================================

def exportar_historico_compras(
    con,
    writer
):

    df = con.execute("""
        SELECT

            codigo_produto,
            data_compra,
            codigo_fornecedor,
            custo_unitario,
            quantidade,
            custo_total

        FROM tb_historico_compras

        ORDER BY
            codigo_produto,
            data_compra

    """).df()

    df.to_excel(
        writer,
        sheet_name="Evolução Histórica",
        index=False
    )

    print(
        "Aba criada: Evolução Histórica"
    )


def run(
    caminho_banco,
    idioma="PT"
):
    
    if idioma.upper() == "EN":

        abas = {
            "resumo": "Executive Summary",
            "compras": "Monthly Purchases",
            "top_fornecedores": "Top Suppliers",
            "abc_fornecedores": "Supplier ABC Analysis",
            "top_produtos": "Top Products",
            "base_produtos": "Product Database",
            "abc_produtos": "Product ABC Analysis",
            "top_savings": "Top Opportunities",
            "saving_completo": "Savings Opportunities",
            "inflacao": "Price Variation",
            "historico": "Historical Evolution"
        }

    else:

        abas = {
            "resumo": "Resumo Executivo",
            "compras": "Compras Mensais",
            "top_fornecedores": "Top Fornecedores",
            "abc_fornecedores": "ABC Fornecedores",
            "top_produtos": "Top Produtos",
            "base_produtos": "Base Produtos",
            "abc_produtos": "ABC Produtos",
            "top_savings": "Top Oportunidades",
            "saving_completo": "Oportunidades de Economia",
            "inflacao": "Variação de Preços",
            "historico": "Evolução Histórica"
        }
    
    
    
    

    print(
        f"IDIOMA RELATORIO = {idioma}"
    )

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )


    arquivo_saida = (
        "compras_inteligencia_relatorio.xlsx"
    )

    with pd.ExcelWriter(
        arquivo_saida,
        engine="openpyxl"
    ) as writer:

        # ====================================================
        # RESUMO EXECUTIVO
        # ====================================================

        df = con.execute("""
            SELECT *
            FROM tb_relatorio_executivo
        """).df()

        df.to_excel(
            writer,
            sheet_name=abas["resumo"],
            index=False
        )

        print(
            "Aba criada: Resumo Executivo"
        )

        # ====================================================
        # COMPRAS MENSAIS
        # ====================================================

        df = con.execute("""
            SELECT *
            FROM tb_compras_mensais
            ORDER BY ano_mes
        """).df()

        df.to_excel(
            writer,
            sheet_name=abas["compras"],
            index=False
        )

        print(
            "Aba criada: Compras Mensais"
        )

        # ====================================================
        # TOP FORNECEDORES
        # ====================================================

        df = con.execute("""
            SELECT *
            FROM tb_ranking_fornecedores
            ORDER BY ranking
            LIMIT 20
        """).df()

        df.to_excel(
            writer,
            sheet_name=abas["top_fornecedores"],
            index=False
        )

        print(
            "Aba criada: Top Fornecedores"
        )

        # ====================================================
        # ABC FORNECEDORES
        # ====================================================

        df = con.execute("""
            SELECT *
            FROM tb_curva_abc_fornecedores
            ORDER BY ranking
        """).df()

        df.to_excel(
            writer,
            sheet_name=abas["abc_fornecedores"],
            index=False
        )

        print(
            "Aba criada: ABC Fornecedores"
        )

        # ====================================================
        # TOP PRODUTOS
        # ====================================================

        df = con.execute("""
            SELECT *
            FROM tb_ranking_produtos
            ORDER BY ranking
            LIMIT 100
        """).df()

        df.to_excel(
            writer,
            sheet_name=abas["top_produtos"],
            index=False
        )

        print(
            "Aba criada: Top Produtos"
        )

        # ====================================================
        # BASE PRODUTOS
        # ====================================================

        df = con.execute("""
            SELECT *
            FROM tb_ranking_produtos
            ORDER BY ranking
        """).df()

        df.to_excel(
            writer,
            sheet_name=abas["base_produtos"],
            index=False
        )

        print(
            "Aba criada: Base Produtos"
        )

        # ====================================================
        # ABC PRODUTOS
        # ====================================================

        df = con.execute("""
            SELECT *
            FROM tb_curva_abc_produtos
            ORDER BY ranking
        """).df()

        df.to_excel(
            writer,
            sheet_name=abas["abc_produtos"],
            index=False
        )

        print(
            "Aba criada: ABC Produtos"
        )

        # ====================================================
        # TOP SAVINGS
        # ====================================================

        df = con.execute("""
            SELECT *
            FROM tb_ranking_saving
            ORDER BY ranking
            LIMIT 50
        """).df()

        df.to_excel(
            writer,
            sheet_name="Top Oportunidades",
            index=False
        )

        print(
            "Aba criada: Top Oportunidades"
        )

        # ====================================================
        # SAVING COMPLETO
        # ====================================================

        df = con.execute("""
            SELECT *
            FROM tb_ranking_saving
            ORDER BY ranking
        """).df()

        df.to_excel(
            writer,
            sheet_name="Oportunidades de Economia",
            index=False
        )

        print(
            "Aba criada: Oportunidades de Economia"
        )

        # ====================================================
        # INFLAÇÃO
        # ====================================================

        df = con.execute("""
            SELECT *
            FROM tb_inflacao_compras
            ORDER BY ano_mes
        """).df()

        df.to_excel(
            writer,
            sheet_name="Variação de Preços",
            index=False
        )

        print(
            "Aba criada: Variação de Preços"
        )

        # ====================================================
        # EVOLUÇÃO HISTÓRICA
        # ====================================================

        exportar_historico_compras(
            con,
            writer
        )


    con.close()

    print(
        f"Relatório criado: "
        f"{arquivo_saida}"
    )

    return arquivo_saida