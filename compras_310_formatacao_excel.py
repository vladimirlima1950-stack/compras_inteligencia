# compras_310_formatacao_excel.py
# ============================================================
# FORMATAÇÃO DO RELATÓRIO EXCEL
# ============================================================

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill


# ============================================================
# CONFIGURAÇÕES DE IDIOMA, ABAS E FORMATOS
# ============================================================
def obter_abas(idioma="PT"):
    if idioma.upper() == "EN":
        return {
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
            "historico": "Historical Evolution",
        }
    return {
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
        "historico": "Evolução Histórica",
    }


def obter_textos(idioma="PT"):
    if idioma.upper() == "EN":
        return {
            "Ano": "Year",
            "Ano-Mês": "Year-Month",
            "Classe ABC": "ABC Class",
            "Código do Item": "SKU",
            "Custo Atual": "Current Cost",
            "Custo Total": "Total Cost",
            "Custo Unitário": "Unit Cost",
            "Data da Compra": "Purchase Date",
            "Fornecedor": "Supplier",
            "Fornecedor Atual": "Current Supplier",
            "Fornecedor Menor Custo Histórico": "Lowest-Cost Historical Supplier",
            "Fornecedores": "Suppliers",
            "Indicador": "Indicator",
            "Itens Avaliados": "Items Evaluated",
            "Itens com Aumento": "Items with Price Increase",
            "Itens com Redução": "Items with Price Reduction",
            "Menor Custo Histórico": "Lowest Historical Cost",
            "Mês": "Month",
            "Participação (%)": "Share (%)",
            "Participação Acumulada (%)": "Cumulative Share (%)",
            "Potencial Economia (%)": "Savings Potential (%)",
            "Potencial Economia ($)": "Savings Potential ($)",
            "Produto": "SKU",
            "Produtos": "SKUs",
            "Quantidade": "Quantity",
            "Quantidade Comprada": "Purchased Quantity",
            "Ranking": "Rank",
            "Registros": "Records",
            "Status": "Status",
            "Último Mês": "Most Recent Purchase Month",
            "Valor": "Value",
            "Valor Comprado": "Purchase Value",
            "Variação Média dos Preços(%)": "Average Price Change (%)",
        }

    return {
        "Ano": "Ano",
        "Ano-Mês": "Ano-Mês",
        "Classe ABC": "Classe ABC",
        "Código do Item": "Código do Item",
        "Custo Atual": "Custo Atual",
        "Custo Total": "Custo Total",
        "Custo Unitário": "Custo Unitário",
        "Data da Compra": "Data da Compra",
        "Fornecedor": "Fornecedor",
        "Fornecedor Atual": "Fornecedor Atual",
        "Fornecedor Menor Custo Histórico": "Fornecedor Menor Custo Histórico",
        "Fornecedores": "Fornecedores",
        "Indicador": "Indicador",
        "Itens Avaliados": "Itens Avaliados",
        "Itens com Aumento": "Itens com Aumento",
        "Itens com Redução": "Itens com Redução",
        "Menor Custo Histórico": "Menor Custo Histórico",
        "Mês": "Mês",
        "Participação (%)": "Participação (%)",
        "Participação Acumulada (%)": "Participação Acumulada (%)",
        "Potencial Economia (%)": "Potencial Economia (%)",
        "Potencial Economia ($)": "Potencial Economia ($)",
        "Produto": "Produto",
        "Produtos": "Produtos",
        "Quantidade": "Quantidade",
        "Quantidade Comprada": "Quantidade Comprada",
        "Ranking": "Ranking",
        "Registros": "Registros",
        "Status": "Status",
        "Último Mês": "Último Mês",
        "Valor": "Valor",
        "Valor Comprado": "Valor Comprado",
        "Variação Média dos Preços(%)": "Variação Média dos Preços(%)",
    }


def obter_formatos(idioma="PT"):
    en = idioma.upper() == "EN"
    return {
        "inteiro": "#,##0",
        "decimal_2": "#,##0.00",
        "custo_unit": "#,##0.0000",
        "percentual": "#,##0.00",
        "percentual_resumo": '#,##0.00"%"',
        "data": "mm/dd/yyyy" if en else "dd/mm/yyyy",
        "texto": "@",
    }


# ============================================================
# UTILITÁRIOS GENÉRICOS DE ESTILO E FORMATAÇÃO
# ============================================================
def ajustar_largura(ws):
    for coluna in ws.columns:
        largura = 0
        letra_coluna = coluna[0].column_letter
        for celula in coluna:
            try:
                if celula.value is not None:
                    largura = max(largura, len(str(celula.value)))
            except Exception:
                pass
        ws.column_dimensions[letra_coluna].width = largura + 3


def formatar_cabecalho(ws):
    azul = PatternFill("solid", fgColor="1F4E78")
    fonte = Font(color="FFFFFF", bold=True)
    alinhamento = Alignment(horizontal="center")

    for celula in ws[1]:
        celula.fill = azul
        celula.font = fonte
        celula.alignment = alinhamento


def formatar_aba_tabular(ws, mapa_cabecalhos, mapa_formatos, formatos):
    # 1. Traduz/renomeia os cabeçalhos da linha 1
    for celula in ws[1]:
        if celula.value in mapa_cabecalhos:
            celula.value = mapa_cabecalhos[celula.value]

    # 2. Localiza índices das colunas pelo nome já traduzido
    indices_formato = {}
    for idx, celula in enumerate(ws[1], start=1):
        nome_coluna = celula.value
        if nome_coluna in mapa_formatos:
            chave_fmt = mapa_formatos[nome_coluna]
            indices_formato[idx] = formatos[chave_fmt]

    # 3. Aplica máscaras nas linhas de dados
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        for col_idx, num_fmt in indices_formato.items():
            celula = row[col_idx - 1]
            if celula.value is not None:
                celula.number_format = num_fmt


def colorir_coluna_por_mapa(ws, nome_coluna, cores_por_valor):
    col_idx = None
    for idx, celula in enumerate(ws[1], start=1):
        if celula.value == nome_coluna:
            col_idx = idx
            break

    if col_idx is None:
        return

    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        celula = row[col_idx - 1]
        cor = cores_por_valor.get(celula.value)
        if cor:
            celula.fill = PatternFill("solid", fgColor=cor)


# ============================================================
# FORMATAÇÃO DO RESUMO EXECUTIVO (PIVOT VERTICAL)
# ============================================================
def reconstruir_resumo(ws, idioma="PT"):
    t = obter_textos(idioma)
    fmt = obter_formatos(idioma)
    en = idioma.upper() == "EN"

    dados = {}
    if ws.max_row >= 2:
        cabecalhos = [celula.value for celula in ws[1]]
        valores = [celula.value for celula in ws[2]]
        dados = dict(zip(cabecalhos, valores))

    ws.delete_rows(1, ws.max_row)

    ws["A1"] = t["Indicador"]
    ws["B1"] = t["Valor"]

    definicao = [
        ("Valor Total Comprado", "Total Purchase Value", "valor_total_comprado", "decimal_2"),
        ("Quantidade Comprada", "Total Purchased Quantity", "quantidade_total_comprada", "decimal_2"),
        ("Produtos Distintos", "Distinct SKUs", "produtos_distintos", "inteiro"),
        ("Fornecedores Distintos", "Distinct Suppliers", "fornecedores_distintos", "inteiro"),
        ("Meses Avaliados", "Months Evaluated", "meses_periodo", "inteiro"),
        ("Compra Média Mensal", "Average Monthly Purchase", "compra_media_mensal", "decimal_2"),
        ("Maior Mês", "Highest Month", "maior_mes_compra", "texto"),
        ("Valor do Maior Mês", "Highest Month Value", "valor_maior_mes", "decimal_2"),
        ("Menor Mês", "Lowest Month", "menor_mes_compra", "texto"),
        ("Valor do Menor Mês", "Lowest Month Value", "valor_menor_mes", "decimal_2"),
        ("IPCA Acumulado", "CPI Accumulated", "ipca_acumulado", "percentual_resumo"),
        ("IGPM Acumulado", "PPI Finished Goods Accumulated", "igpm_acumulado", "percentual_resumo"),
        ("IPAM Acumulado", "PPI Commodities Accumulated", "ipam_acumulado", "percentual_resumo"),
        ("IPADI Acumulado", "PPI Intermediate Accumulated", "ipadi_acumulado", "percentual_resumo"),
        ("Oportunidades Totais", "Total Opportunities", "oportunidades_totais", "inteiro"),
        ("Oportunidades Normais", "Normal Opportunities", "qtd_normal", "inteiro"),
        ("Oportunidades Atenção", "Attention Opportunities", "qtd_atencao", "inteiro"),
        ("Oportunidades Anomalia", "Anomaly Opportunities", "qtd_anomalia", "inteiro"),
        ("Potencial Total de Economia", "Total Savings Potential", "saving_total", "decimal_2"),
        ("Potencial Médio de Economia", "Average Savings Potential", "saving_medio", "decimal_2"),
        ("Maior Potencial de Economia", "Highest Savings Potential", "maior_saving", "decimal_2"),
        ("Maior Potencial de Economia Normal", "Highest Normal Savings Potential", "maior_saving_normal", "decimal_2"),
        ("Maior Potencial de Economia Atenção", "Highest Attention Savings Potential", "maior_saving_atencao", "decimal_2"),
        ("Maior Potencial de Economia Anomalia", "Highest Anomaly Savings Potential", "maior_saving_anomalia", "decimal_2"),
        ("Variação Média dos Preços", "Average Price Change", "inflacao_media_periodo", "percentual_resumo"),
    ]

    for linha, (rotulo_pt, rotulo_en, chave, tipo_fmt) in enumerate(definicao, start=2):
        rotulo = rotulo_en if en else rotulo_pt
        valor = dados.get(chave)

        ws.cell(linha, 1, rotulo)
        cel_valor = ws.cell(linha, 2, valor)
        if valor is not None and tipo_fmt in fmt:
            cel_valor.number_format = fmt[tipo_fmt]


# ============================================================
# ESPECIFICAÇÃO DAS DEMAIS ABAS
# ============================================================
def obter_especificacoes_abas(idioma="PT"):
    t = obter_textos(idioma)

    spec_ranking_fornecedores = (
        {
            "ranking": t["Ranking"],
            "codigo_fornecedor": t["Fornecedor"],
            "fornecedor": t["Fornecedor"],
            "valor_comprado": t["Valor Comprado"],
            "percentual": t["Participação (%)"],
        },
        {
            t["Ranking"]: "inteiro",
            t["Fornecedor"]: "texto",
            t["Valor Comprado"]: "decimal_2",
            t["Participação (%)"]: "percentual",
        },
    )

    spec_abc_fornecedores = (
        {
            "ranking": t["Ranking"],
            "codigo_fornecedor": t["Fornecedor"],
            "valor_comprado": t["Valor Comprado"],
            "percentual": t["Participação (%)"],
            "percentual_acumulado": t["Participação Acumulada (%)"],
            "classe": t["Classe ABC"],
        },
        {
            t["Ranking"]: "inteiro",
            t["Fornecedor"]: "texto",
            t["Valor Comprado"]: "decimal_2",
            t["Participação (%)"]: "percentual",
            t["Participação Acumulada (%)"]: "percentual",
        },
    )

    spec_ranking_produtos = (
        {
            "ranking": t["Ranking"],
            "codigo_produto": t["Produto"],
            "valor_comprado": t["Valor Comprado"],
            "percentual": t["Participação (%)"],
        },
        {
            t["Ranking"]: "inteiro",
            t["Produto"]: "texto",
            t["Valor Comprado"]: "decimal_2",
            t["Participação (%)"]: "percentual",
        },
    )

    spec_abc_produtos = (
        {
            "ranking": t["Ranking"],
            "codigo_produto": t["Produto"],
            "valor_comprado": t["Valor Comprado"],
            "percentual": t["Participação (%)"],
            "percentual_acumulado": t["Participação Acumulada (%)"],
            "classe": t["Classe ABC"],
        },
        {
            t["Ranking"]: "inteiro",
            t["Produto"]: "texto",
            t["Valor Comprado"]: "decimal_2",
            t["Participação (%)"]: "percentual",
            t["Participação Acumulada (%)"]: "percentual",
        },
    )

    spec_saving = (
        {
            "ranking": t["Ranking"],
            "codigo_produto": t["Produto"],
            "codigo_fornecedor": t["Fornecedor Atual"],
            "ultimo_mes": t["Último Mês"],
            "custo_atual": t["Custo Atual"],
            "menor_custo_historico": t["Menor Custo Histórico"],
            "fornecedor_menor_custo_historico": t["Fornecedor Menor Custo Histórico"],
            "saving_absoluto": t["Potencial Economia ($)"],
            "saving_percentual": t["Potencial Economia (%)"],
            "status": t["Status"],
        },
        {
            t["Ranking"]: "inteiro",
            t["Produto"]: "texto",
            t["Fornecedor Atual"]: "texto",
            t["Custo Atual"]: "decimal_2",
            t["Menor Custo Histórico"]: "decimal_2",
            t["Fornecedor Menor Custo Histórico"]: "texto",
            t["Potencial Economia ($)"]: "decimal_2",
            t["Potencial Economia (%)"]: "percentual",
        },
    )

    return {
        "compras": (
            {
                "ano_mes": t["Ano-Mês"],
                "ano": t["Ano"],
                "mes": t["Mês"],
                "valor_comprado": t["Valor Comprado"],
                "quantidade_comprada": t["Quantidade Comprada"],
                "fornecedores": t["Fornecedores"],
                "produtos": t["Produtos"],
                "registros": t["Registros"],
            },
            {
                t["Valor Comprado"]: "decimal_2",
                t["Quantidade Comprada"]: "decimal_2",
                t["Fornecedores"]: "inteiro",
                t["Produtos"]: "inteiro",
                t["Registros"]: "inteiro",
            },
        ),
        "top_fornecedores": spec_ranking_fornecedores,
        "abc_fornecedores": spec_abc_fornecedores,
        "top_produtos": spec_ranking_produtos,
        "base_produtos": spec_ranking_produtos,
        "abc_produtos": spec_abc_produtos,
        "top_savings": spec_saving,
        "saving_completo": spec_saving,
        "inflacao": (
            {
                "ano_mes": t["Ano-Mês"],
                "itens_avaliados": t["Itens Avaliados"],
                "itens_com_aumento": t["Itens com Aumento"],
                "itens_com_reducao": t["Itens com Redução"],
                "inflacao_media": t["Variação Média dos Preços(%)"],
            },
            {
                t["Itens Avaliados"]: "inteiro",
                t["Itens com Aumento"]: "inteiro",
                t["Itens com Redução"]: "inteiro",
                t["Variação Média dos Preços(%)"]: "percentual",
            },
        ),
        "historico": (
            {
                "codigo_produto": t["Código do Item"],
                "data_compra": t["Data da Compra"],
                "codigo_fornecedor": t["Fornecedor"],
                "custo_unitario": t["Custo Unitário"],
                "quantidade": t["Quantidade"],
                "custo_total": t["Custo Total"],
            },
            {
                t["Código do Item"]: "texto",
                t["Data da Compra"]: "data",
                t["Fornecedor"]: "texto",
                t["Custo Unitário"]: "custo_unit",
                t["Quantidade"]: "inteiro",
                t["Custo Total"]: "decimal_2",
            },
        ),
    }


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================
def run(arquivo_excel, idioma="PT"):
    abas = obter_abas(idioma)
    t = obter_textos(idioma)
    fmt = obter_formatos(idioma)
    specs = obter_especificacoes_abas(idioma)

    wb = load_workbook(arquivo_excel)
    print(f"IDIOMA FORMATACAO = {idioma}")

    # 1. Resumo Executivo
    if abas["resumo"] in wb.sheetnames:
        reconstruir_resumo(wb[abas["resumo"]], idioma)

    # 2. Abas tabulares
    for chave_aba, (mapa_cabecalhos, mapa_formatos) in specs.items():
        nome_aba = abas[chave_aba]
        if nome_aba in wb.sheetnames:
            formatar_aba_tabular(
                wb[nome_aba],
                mapa_cabecalhos,
                mapa_formatos,
                fmt,
            )

    # 3. Formatação visual comum a todas as abas
    for ws in wb.worksheets:
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        formatar_cabecalho(ws)
        ajustar_largura(ws)

    # 4. Destaques condicionais por cor
    cores_abc = {
        "A": "92D050",
        "B": "FFD966",
        "C": "FF9999",
    }
    for chave_abc in ("abc_fornecedores", "abc_produtos"):
        nome_aba = abas[chave_abc]
        if nome_aba in wb.sheetnames:
            colorir_coluna_por_mapa(wb[nome_aba], t["Classe ABC"], cores_abc)

    cores_status = {
        "NORMAL": "92D050",
        "ATENCAO": "FFD966",
        "ANOMALIA": "FF9999",
    }
    for chave_saving in ("top_savings", "saving_completo"):
        nome_aba = abas[chave_saving]
        if nome_aba in wb.sheetnames:
            colorir_coluna_por_mapa(wb[nome_aba], t["Status"], cores_status)

    wb.save(arquivo_excel)
    print("Excel formatado com sucesso.")
    return arquivo_excel