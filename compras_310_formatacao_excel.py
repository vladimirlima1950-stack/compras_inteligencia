# compras_310_formatacao_excel.py

# ============================================================
# FORMATAÇÃO DO RELATÓRIO EXCEL
# ============================================================

from openpyxl import load_workbook
from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment
)


def obter_textos(idioma="PT"):

    if idioma.upper() == "EN":

        return {

            "Ano": "Year",
            "Ano-Mês": "Year-Month",

            "Classe ABC": "ABC Class",
            
            "Código do Item": "SKU",

            "Custo Atual": "Current Cost",
            
            "Custo Total": "Total Cost",

            "Data da Compra": "Purchase Date",

            "Fornecedor": "Supplier",
            "Fornecedor Atual": "Current Supplier",
            "Fornecedor Menor Custo Histórico":
                "Lowest-Cost Historical Supplier",

            "Fornecedores": "Suppliers",

            "Indicador": "Indicator",

            "Itens Avaliados": "Items Evaluated",
            "Itens com Aumento":
                "Items with Price Increase",
            "Itens com Redução":
                "Items with Price Reduction",

            "Menor Custo Histórico":
                "Lowest Historical Cost",

            "Mês": "Month",

            "Participação (%)":
                "Share (%)",

            "Participação Acumulada (%)":
                "Cumulative Share (%)",

            "Potencial Economia (%)":
                "Savings Potential (%)",

            "Potencial Economia ($)":
                "Savings Potential ($)",

            "Produto": "SKU",
            "Produtos": "SKUs",

            "Quantidade Comprada":
                "Purchased Quantity",
                
            "Quantidade": "Quantity",

            "Ranking": "Rank",

            "Registros": "Records",

            "Status": "Status",

            "Último Mês":
                "Most Recent Purchase Month",
            "Custo Unitário": "Unit Cost",

            "Valor": "Value",

            "Valor Comprado":
                "Purchase Value",

            "Variação Média dos Preços(%)":
                "Average Price Change (%)"

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
        "Fornecedor Menor Custo Histórico":
            "Fornecedor Menor Custo Histórico",

        "Fornecedores": "Fornecedores",

        "Indicador": "Indicador",

        "Itens Avaliados": "Itens Avaliados",
        "Itens com Aumento": "Itens com Aumento",
        "Itens com Redução": "Itens com Redução",

        "Menor Custo Histórico":
            "Menor Custo Histórico",

        "Mês": "Mês",

        "Participação (%)":
            "Participação (%)",

        "Participação Acumulada (%)":
            "Participação Acumulada (%)",

        "Potencial Economia (%)":
            "Potencial Economia (%)",

        "Potencial Economia ($)":
            "Potencial Economia ($)",

        "Produto": "Produto",
        "Produtos": "Produtos",
        
        "Quantidade": "Quantidade",

        "Quantidade Comprada":
            "Quantidade Comprada",

        "Ranking": "Ranking",

        "Registros": "Registros",

        "Status": "Status",

        "Último Mês": "Último Mês",

        "Valor": "Valor",

        "Valor Comprado":
            "Valor Comprado",

        "Variação Média dos Preços(%)":
            "Variação Média dos Preços(%)"

    }



def ajustar_largura(ws):

    for coluna in ws.columns:

        largura = 0

        letra_coluna = coluna[0].column_letter

        for celula in coluna:

            try:

                if celula.value:

                    largura = max(
                        largura,
                        len(str(celula.value))
                    )

            except:

                pass

        ws.column_dimensions[
            letra_coluna
        ].width = largura + 3


def formatar_cabecalho(
    ws,
    idioma = "PT"
    ):

    azul = PatternFill(
        "solid",
        fgColor="1F4E78"
    )

    fonte = Font(
        color="FFFFFF",
        bold=True
    )

    for celula in ws[1]:

        celula.fill = azul

        celula.font = fonte

        celula.alignment = Alignment(
            horizontal="center"
        )


def colorir_coluna_abc(ws):

    for row in ws.iter_rows(
        min_row=2
    ):

        for celula in row:

            if celula.value == "A":

                celula.fill = PatternFill(
                    "solid",
                    fgColor="92D050"
                )

            elif celula.value == "B":

                celula.fill = PatternFill(
                    "solid",
                    fgColor="FFD966"
                )

            elif celula.value == "C":

                celula.fill = PatternFill(
                    "solid",
                    fgColor="FF9999"
                )


def colorir_status(ws):

    for row in ws.iter_rows(
        min_row=2
    ):

        for celula in row:

            if celula.value == "NORMAL":

                celula.fill = PatternFill(
                    "solid",
                    fgColor="92D050"
                )

            elif celula.value == "ATENCAO":

                celula.fill = PatternFill(
                    "solid",
                    fgColor="FFD966"
                )

            elif celula.value == "ANOMALIA":

                celula.fill = PatternFill(
                    "solid",
                    fgColor="FF9999"
                )


def reconstruir_resumo(ws, idioma="PT"):
    t = obter_textos(idioma)
    en = idioma.upper() == "EN"

    dados = {}
    cabecalhos = [celula.value for celula in ws[1]]
    valores = [celula.value for celula in ws[2]]

    for chave, valor in zip(cabecalhos, valores):
        dados[chave] = valor

    ws.delete_rows(1, ws.max_row)

    ws["A1"] = t["Indicador"]
    ws["B1"] = t["Valor"]

    # Cada item: (rótulo_pt, rótulo_en, chave_dados, tipo_formato)
    definicao = [
        ("Valor Total Comprado", "Total Purchase Value", "valor_total_comprado", "2_casas"),
        ("Quantidade Comprada", "Total Purchased Quantity", "quantidade_total_comprada", "2_casas"),
        ("Produtos Distintos", "Distinct SKUs", "produtos_distintos", "inteiro"),
        ("Fornecedores Distintos", "Distinct Suppliers", "fornecedores_distintos", "inteiro"),
        ("Meses Avaliados", "Months Evaluated", "meses_periodo", "inteiro"),
        ("Compra Média Mensal", "Average Monthly Purchase", "compra_media_mensal", "2_casas"),
        ("Maior Mês", "Highest Month", "maior_mes_compra", "texto"),
        ("Valor do Maior Mês", "Highest Month Value", "valor_maior_mes", "2_casas"),
        ("Menor Mês", "Lowest Month", "menor_mes_compra", "texto"),
        ("Valor do Menor Mês", "Lowest Month Value", "valor_menor_mes", "2_casas"),
        ("IPCA Acumulado (%)", "CPI Accumulated (%)", "ipca_acumulado", "percentual"),
        ("IGPM Acumulado (%)", "PPI Finished Goods Accumulated (%)", "igpm_acumulado", "percentual"),
        ("IPAM Acumulado (%)", "PPI Commodities Accumulated (%)", "ipam_acumulado", "percentual"),
        ("IPADI Acumulado (%)", "PPI Intermediate Accumulated (%)", "ipadi_acumulado", "percentual"),
        ("Oportunidades Totais", "Total Opportunities", "oportunidades_totais", "inteiro"),
        ("Oportunidades Normais", "Normal Opportunities", "qtd_normal", "inteiro"),
        ("Oportunidades Atenção", "Attention Opportunities", "qtd_atencao", "inteiro"),
        ("Oportunidades Anomalia", "Anomaly Opportunities", "qtd_anomalia", "inteiro"),
        ("Potencial Total de Economia", "Total Savings Potential", "saving_total", "2_casas"),
        ("Potencial Médio de Economia", "Average Savings Potential", "saving_medio", "2_casas"),
        ("Maior Potencial de Economia", "Highest Savings Potential", "maior_saving", "2_casas"),
        ("Maior Potencial de Economia Normal", "Highest Normal Savings Potential", "maior_saving_normal", "2_casas"),
        ("Maior Potencial de Economia Atenção", "Highest Attention Savings Potential", "maior_saving_atencao", "2_casas"),
        ("Maior Potencial de Economia Anomalia", "Highest Anomaly Savings Potential", "maior_saving_anomalia", "2_casas"),
        ("Variação Média dos Preços", "Average Price Change (%)", "inflacao_media_periodo", "percentual"),
    ]

    formatos_por_linha = {}
    linha = 2

    for rotulo_pt, rotulo_en, chave, tipo_fmt in definicao:
        rotulo = rotulo_en if en else rotulo_pt
        valor = dados.get(chave)

        ws.cell(linha, 1, rotulo)
        cel_valor = ws.cell(linha, 2, valor)
        formatos_por_linha[linha] = tipo_fmt
        linha += 1

    formatar_cabecalho(ws, idioma)
    formatar_valores_resumo(ws, idioma, formatos_por_linha)




def formatar_valores_resumo(
    ws,
    idioma = "PT"
    ):

    t = obter_textos(idioma)

    indicadores_2_casas = {
        "Valor Total Comprado",
        "Quantidade Comprada",
        "Compra Média Mensal",
        "Valor do Maior Mês",
        "Valor do Menor Mês",
        

        
        "Potencial Total de Economia",
        "Potencial Médio de Economia",
        "Maior Potencial de Economia",
        "Maior Potencial de Economia Normal",
        "Maior Potencial de Economia Atenção",
        "Maior Potencial de Economia Anomalia",
        "Variação Média dos Preços"
    }



    indicadores_inteiros = {
        "Produtos Distintos",
        "Fornecedores Distintos",
        "Meses Avaliados",
        "Oportunidades Totais",
        "Oportunidades Normais",
        "Oportunidades Atenção",
        "Oportunidades Anomalia"
    }
    
    
    indicadores_percentuais = {
        "IPCA Acumulado (%)",
        "IGPM Acumulado (%)",
        "IPAM Acumulado (%)",
        "IPADI Acumulado (%)",
        "Variação Média dos Preços"
    }

    for row in ws.iter_rows(min_row=2):

        indicador = row[0].value
        valor = row[1]

        if indicador in indicadores_percentuais:
            valor.number_format = '#,##0.00"%"'
    
        

        elif indicador in indicadores_2_casas:
            valor.number_format = '#,##0.00'


        elif indicador in indicadores_inteiros:
            valor.number_format = '#,##0'

    
    
def formatar_compras_mensais(
    ws,
    idioma = "PT"
    ):

    t = obter_textos(idioma)

    cabecalhos = {
        "ano_mes": t["Ano-Mês"],
        "ano": t["Ano"],
        "mes": t["Mês"],
        "valor_comprado": t["Valor Comprado"],
        "quantidade_comprada": t["Quantidade Comprada"],
        "fornecedores": t["Fornecedores"],
        "produtos": t["Produtos"],
        "registros": t["Registros"]
    }

    for celula in ws[1]:
        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]

    for row in ws.iter_rows(min_row=2):

        row[3].number_format = '#,##0.00'
        row[4].number_format = '#,##0.00'

        row[5].number_format = '#,##0'
        row[6].number_format = '#,##0'
        row[7].number_format = '#,##0'

def formatar_top_fornecedores(
    ws,
    idioma="PT"
    ):
        
    t = obter_textos(idioma)

    cabecalhos = {
        "ranking": t["Ranking"],
        "fornecedor": t["Fornecedor"],
        "valor_comprado": t["Valor Comprado"],
        "percentual": t["Participação (%)"]
    }

    for celula in ws[1]:

        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]

    for row in ws.iter_rows(min_row=2):

        row[0].number_format = '#,##0'

        row[2].number_format = '#,##0.00'

        row[3].number_format = '#,##0.00'



def formatar_abc_fornecedores(
    ws,
    idioma = "PT"
    ):
        
    t = obter_textos(idioma)

    cabecalhos = {
        "ranking": t["Ranking"],
        "codigo_fornecedor": t["Fornecedor"],
        "valor_comprado": t["Valor Comprado"],
        "percentual": t["Participação (%)"],
        "percentual_acumulado": t["Participação Acumulada (%)"],
        "classe": t["Classe ABC"]
    }

    for celula in ws[1]:
    
        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]
    

    for row in ws.iter_rows(min_row=2):

        row[0].number_format = '#,##0'

        row[2].number_format = '#,##0.00'

        row[3].number_format = '#,##0.00'

        row[4].number_format = '#,##0.00'


def formatar_top_produtos(
        ws,
        idioma="PT"
        ):

    t = obter_textos(idioma)


    cabecalhos = {
        "ranking": t["Ranking"],

        "codigo_produto": t["Produto"],

        "valor_comprado": t["Valor Comprado"],

        "percentual": t["Participação (%)"]
        
        
    }

    for celula in ws[1]:

        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]

    for row in ws.iter_rows(min_row=2):

        row[0].number_format = '#,##0'

        row[2].number_format = '#,##0.00'

        row[3].number_format = '#,##0.00'

def formatar_base_produtos(
    ws,
    idioma = "PT"
):

    t = obter_textos(idioma)
    
    cabecalhos = {
        "ranking": t["Ranking"],
        "codigo_produto": t["Produto"],
        "valor_comprado": t["Valor Comprado"],
        "percentual": t["Participação (%)"]
    }   
    
    for celula in ws[1]:

        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]

    for row in ws.iter_rows(min_row=2):

        row[0].number_format = '#,##0'

        row[2].number_format = '#,##0.00'

        row[3].number_format = '#,##0.00'

def formatar_abc_produtos(
    ws,
    idioma = "PT"
    ):
        
        
    t = obter_textos(idioma)

    cabecalhos = {
        "ranking": t["Ranking"],
        "codigo_produto": t["Produto"],
        "valor_comprado": t["Valor Comprado"],
        "percentual": t["Participação (%)"],
        "percentual_acumulado": t["Participação Acumulada (%)"],
        "classe": t["Classe ABC"]
    }

    for celula in ws[1]:

        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]

    for row in ws.iter_rows(min_row=2):

        row[0].number_format = '#,##0'

        row[2].number_format = '#,##0.00'

        row[3].number_format = '#,##0.00'

        row[4].number_format = '#,##0.00'





    
def formatar_top_savings(
    ws,
    idioma = "PT"
    ):
        
    t = obter_textos(idioma)

    cabecalhos = {

        "ranking": t["Ranking"],

        "codigo_produto": t["Produto"],

        "codigo_fornecedor": t["Fornecedor Atual"],

        "ultimo_mes": t["Último Mês"],

        "custo_atual": t["Custo Atual"],

        "menor_custo_historico":
            t["Menor Custo Histórico"],

        "fornecedor_menor_custo_historico":
            t["Fornecedor Menor Custo Histórico"],

        "saving_absoluto":
            t["Potencial Economia ($)"],

        "saving_percentual":
            t["Potencial Economia (%)"],

        "status": t["Status"]
    }

    for celula in ws[1]:
        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]

    for row in ws.iter_rows(min_row=2):

        # Ranking
        row[0].number_format = '#,##0'

        # Fornecedor Atual
        row[2].number_format = '@'

        # Custo Atual
        row[4].number_format = '#,##0.00'

        # Menor Custo Histórico
        row[5].number_format = '#,##0.00'

        # Fornecedor Menor Custo Histórico
        row[6].number_format = '@'

        # Potencial Economia ($)
        row[7].number_format = '#,##0.00'

        # Potencial Economia (%)
        row[8].number_format = '#,##0.00'



def formatar_saving_completo(
    ws,
    idioma = "PT"
    ):
    
    t = obter_textos(idioma)

    
    cabecalhos = {

        "ranking": t["Ranking"],

        "codigo_produto": t["Produto"],

        "codigo_fornecedor": t["Fornecedor Atual"],

        "ultimo_mes": t["Último Mês"],

        "custo_atual": t["Custo Atual"],

        "menor_custo_historico":
            t["Menor Custo Histórico"],

        "fornecedor_menor_custo_historico":
            t["Fornecedor Menor Custo Histórico"],

        "saving_absoluto":
            t["Potencial Economia ($)"],

        "saving_percentual":
            t["Potencial Economia (%)"],

        "status": t["Status"]
    }
    
    
    
    for celula in ws[1]:
        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]


    for row in ws.iter_rows(min_row=2):

        # Ranking
        row[0].number_format = '#,##0'

        # Fornecedor Atual
        row[2].number_format = '@'

        # Custo Atual
        row[4].number_format = '#,##0.00'

        # Menor Custo Histórico
        row[5].number_format = '#,##0.00'

        # Fornecedor Menor Custo Histórico
        row[6].number_format = '@'

        # Potencial Economia ($)
        row[7].number_format = '#,##0.00'

        # Potencial Economia (%)
        row[8].number_format = '#,##0.00'



def formatar_inflacao(
    ws,
    idioma = "PT"
    ):

    t = obter_textos(idioma)

    cabecalhos = {
        "ano_mes": t["Ano-Mês"],
        "itens_avaliados": t["Itens Avaliados"],
        "itens_com_aumento": t["Itens com Aumento"],
        "itens_com_reducao": t["Itens com Redução"],
        "inflacao_media": t["Variação Média dos Preços(%)]"
    }

    for celula in ws[1]:

        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]

    for row in ws.iter_rows(min_row=2):

        row[1].number_format = '#,##0'
        row[2].number_format = '#,##0'
        row[3].number_format = '#,##0'

        row[4].number_format = '#,##0.00'



def formatar_evolucao_historica(
    ws,
    idioma="PT"
    ):
        
    t = obter_textos(idioma)

    cabecalhos = {
        "codigo_produto": t["Código do Item"],
        "data_compra": t["Data da Compra"],
        "codigo_fornecedor": t["Fornecedor"],
        "custo_unitario": t["Custo Unitário"],
        "quantidade": t["Quantidade"],
        "custo_total": t["Custo Total"]
    }

    for celula in ws[1]:

        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]

    for row in ws.iter_rows(min_row=2):

        # Data
        if idioma.upper() == "EN":
            row[1].number_format = 'mm/dd/yyyy'
        else:
            row[1].number_format = 'dd/mm/yyyy'

        # Custo Unitário
        row[3].number_format = '#,##0.0000'

        # Quantidade
        row[4].number_format = '#,##0'

        # Custo Total
        row[5].number_format = '#,##0.00'




    
def run(
    arquivo_excel,
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
    
    
    
    
    
    wb = load_workbook(
        arquivo_excel
    )
 
    print(
        f"IDIOMA FORMATACAO = {idioma}"
    )
    


    # ========================================================
    # RESUMO EXECUTIVO
    # ========================================================

    
    
    ws = wb[abas["resumo"]]

    reconstruir_resumo(ws, idioma)
    
    if abas["compras"] in wb.sheetnames:
        formatar_compras_mensais(
            wb[abas["compras"]],
            idioma
        )

    if abas["top_fornecedores"] in wb.sheetnames:

        formatar_top_fornecedores(
            wb[abas["top_fornecedores"]],
            idioma
        )

    if abas["abc_fornecedores"] in wb.sheetnames:
        formatar_abc_fornecedores(
            wb[abas["abc_fornecedores"]],
            idioma
        )

    if abas["top_produtos"] in wb.sheetnames:

        formatar_top_produtos(
            wb[abas["top_produtos"]],
            idioma
        )


    if abas["base_produtos"] in wb.sheetnames:

        formatar_base_produtos(
            wb[abas["base_produtos"]],
            idioma
        )

    if abas["top_savings"] in wb.sheetnames:
        
         formatar_top_savings(
            wb[abas["top_savings"]],
            idioma
        )

    if abas["saving_completo"] in wb.sheetnames:

        formatar_saving_completo(
            wb[abas["saving_completo"]],
            idioma
        )



    if abas["inflacao"] in wb.sheetnames:

        formatar_inflacao(
            wb[abas["inflacao"]],
            idioma
        )

    if abas["abc_produtos"] in wb.sheetnames:

        formatar_abc_produtos(
            wb[abas["abc_produtos"]],
            idioma
        )

    if abas["historico"] in wb.sheetnames:

        formatar_evolucao_historica(
            wb[abas["historico"]],
            idioma
        )



    # ========================================================
    # TODAS AS ABAS
    # ========================================================

    for ws in wb.worksheets:

        ws.freeze_panes = "A2"

        ws.auto_filter.ref = (
            ws.dimensions
        )

        formatar_cabecalho(ws)
        

        ajustar_largura(ws)

    # ========================================================
    # ABC
    # ========================================================

    if abas["abc_fornecedores"] in wb.sheetnames:

        colorir_coluna_abc(
            wb[abas["abc_fornecedores"]]
        )

    if abas["abc_produtos"] in wb.sheetnames:

        colorir_coluna_abc(
            wb[abas["abc_produtos"]]
        )

    # ========================================================
    # SAVING
    # ========================================================

    if abas["saving_completo"] in wb.sheetnames:

        colorir_status(
            wb[abas["saving_completo"]]
        )

    # ========================================================
    # SALVAR
    # ========================================================

    wb.save(
        arquivo_excel
    )

    print(
        "Excel formatado com sucesso."
    )

    return arquivo_excel
