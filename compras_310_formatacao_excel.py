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


def formatar_cabecalho(ws):

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


def reconstruir_resumo(ws):

    dados = {}

    cabecalhos = []

    valores = []

    for celula in ws[1]:

        cabecalhos.append(
            celula.value
        )

    for celula in ws[2]:

        valores.append(
            celula.value
        )

    for chave, valor in zip(
        cabecalhos,
        valores
    ):

        dados[chave] = valor

    ws.delete_rows(
        1,
        ws.max_row
    )

    ws["A1"] = "Indicador"
    ws["B1"] = "Valor"

    indicadores = [

        ("Valor Total Comprado",
         dados["valor_total_comprado"]),

        ("Quantidade Comprada",
         dados["quantidade_total_comprada"]),

        ("Produtos Distintos",
         dados["produtos_distintos"]),

        ("Fornecedores Distintos",
         dados["fornecedores_distintos"]),

        ("Meses Avaliados",
         dados["meses_periodo"]),

        ("Compra Média Mensal",
         dados["compra_media_mensal"]),

        ("Maior Mês",
         dados["maior_mes_compra"]),

        ("Valor do Maior Mês",
         dados["valor_maior_mes"]),

        ("Menor Mês",
         dados["menor_mes_compra"]),

        ("Valor do Menor Mês",
         dados["valor_menor_mes"]),

        ("Oportunidades Totais",
         dados["oportunidades_totais"]),

        ("Oportunidades Normais",
         dados["qtd_normal"]),

        ("Oportunidades Atenção",
         dados["qtd_atencao"]),

        ("Oportunidades Anomalia",
         dados["qtd_anomalia"]),

        ("Potencial Total de Economia",
         dados["saving_total"]),

        ("Potencial Médio de Economia",
         dados["saving_medio"]),

        ("Maior Potencial de Economia",
         dados["maior_saving"]),

        ("Maior Potencial de Economia Normal",
         dados["maior_saving_normal"]),

        ("Maior Potencial de Economia Atenção",
         dados["maior_saving_atencao"]),

        ("Maior Potencial de Economia Anomalia",
         dados["maior_saving_anomalia"]),

        ("Variação Média dos Preços",
         dados["inflacao_media_periodo"])

    ]

    linha = 2

    for indicador, valor in indicadores:

        ws.cell(
            linha,
            1,
            indicador
        )

        ws.cell(
            linha,
            2,
            valor
        )

        linha += 1

    formatar_cabecalho(ws)
    formatar_valores_resumo(ws)


def formatar_valores_resumo(ws):


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

    for row in ws.iter_rows(min_row=2):

        indicador = row[0].value
        valor = row[1]

        if indicador in indicadores_2_casas:
            valor.number_format = '#,##0.00'

        elif indicador in indicadores_inteiros:
            valor.number_format = '#,##0'

    
    
def formatar_compras_mensais(ws):

    cabecalhos = {
        "ano_mes": "Ano-Mês",
        "ano": "Ano",
        "mes": "Mês",
        "valor_comprado": "Valor Comprado",
        "quantidade_comprada": "Quantidade Comprada",
        "fornecedores": "Fornecedores",
        "produtos": "Produtos",
        "registros": "Registros"
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

def formatar_top_fornecedores(ws):

    cabecalhos = {
        "ranking": "Ranking",
        "codigo_fornecedor": "Fornecedor",
        "valor_comprado": "Valor Comprado",
        "percentual": "Participação (%)"
    }

    for celula in ws[1]:

        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]

    for row in ws.iter_rows(min_row=2):

        row[0].number_format = '#,##0'

        row[2].number_format = '#,##0.00'

        row[3].number_format = '#,##0.00'



def formatar_abc_fornecedores(ws):

    cabecalhos = {
        "ranking": "Ranking",
        "codigo_fornecedor": "Fornecedor",
        "valor_comprado": "Valor Comprado",
        "percentual": "Participação (%)",
        "percentual_acumulado": "Participação Acumulada (%)",
        "classe": "Classe ABC"
    }

    for celula in ws[1]:
    
        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]
    

    for row in ws.iter_rows(min_row=2):

        row[0].number_format = '#,##0'

        row[2].number_format = '#,##0.00'

        row[3].number_format = '#,##0.00'

        row[4].number_format = '#,##0.00'


def formatar_top_produtos(ws):

    cabecalhos = {
        "ranking": "Ranking",
        "codigo_produto": "Produto",
        "valor_comprado": "Valor Comprado",
        "percentual": "Participação (%)"
    }

    for celula in ws[1]:

        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]

    for row in ws.iter_rows(min_row=2):

        row[0].number_format = '#,##0'

        row[2].number_format = '#,##0.00'

        row[3].number_format = '#,##0.00'

def formatar_base_produtos(ws):

    cabecalhos = {
        "ranking": "Ranking",
        "codigo_produto": "Produto",
        "valor_comprado": "Valor Comprado",
        "percentual": "Participação (%)"
    }

    for celula in ws[1]:

        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]

    for row in ws.iter_rows(min_row=2):

        row[0].number_format = '#,##0'

        row[2].number_format = '#,##0.00'

        row[3].number_format = '#,##0.00'

def formatar_abc_produtos(ws):

    cabecalhos = {
        "ranking": "Ranking",
        "codigo_produto": "Produto",
        "valor_comprado": "Valor Comprado",
        "percentual": "Participação (%)",
        "percentual_acumulado": "Participação Acumulada (%)",
        "classe": "Classe ABC"
    }

    for celula in ws[1]:

        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]

    for row in ws.iter_rows(min_row=2):

        row[0].number_format = '#,##0'

        row[2].number_format = '#,##0.00'

        row[3].number_format = '#,##0.00'

        row[4].number_format = '#,##0.00'





    
def formatar_top_savings(ws):
    
    

    cabecalhos = {

        "ranking": "Ranking",

        "codigo_produto": "Produto",

        "codigo_fornecedor": "Fornecedor Atual",

        "ultimo_mes": "Último Mês",

        "custo_atual": "Custo Atual",

        "menor_custo_historico":
            "Menor Custo Histórico",

        "fornecedor_menor_custo_historico":
            "Fornecedor Menor Custo Histórico",

        "saving_absoluto":
            "Potencial Economia (R$)",

        "saving_percentual":
            "Potencial Economia (%)",

        "status": "Status"
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

        # Potencial Economia (R$)
        row[7].number_format = '#,##0.00'

        # Potencial Economia (%)
        row[8].number_format = '#,##0.00'



def formatar_saving_completo(ws):
    
    

    
    cabecalhos = {

        "ranking": "Ranking",

        "codigo_produto": "Produto",

        "codigo_fornecedor": "Fornecedor Atual",

        "ultimo_mes": "Último Mês",

        "custo_atual": "Custo Atual",

        "menor_custo_historico":
            "Menor Custo Histórico",

        "fornecedor_menor_custo_historico":
            "Fornecedor Menor Custo Histórico",

        "saving_absoluto":
            "Potencial Economia (R$)",

        "saving_percentual":
            "Potencial Economia (%)",

        "status": "Status"
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

        # Potencial Economia (R$)
        row[7].number_format = '#,##0.00'

        # Potencial Economia (%)
        row[8].number_format = '#,##0.00'



def formatar_inflacao(ws):

    cabecalhos = {
        "ano_mes": "Ano-Mês",
        "itens_avaliados": "Itens Avaliados",
        "itens_com_aumento": "Itens com Aumento",
        "itens_com_reducao": "Itens com Redução",
        "inflacao_media": "Variação Média dos Preços(%)"
    }

    for celula in ws[1]:

        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]

    for row in ws.iter_rows(min_row=2):

        row[1].number_format = '#,##0'
        row[2].number_format = '#,##0'
        row[3].number_format = '#,##0'

        row[4].number_format = '#,##0.00'



def formatar_evolucao_historica(ws):

    cabecalhos = {
        "codigo_produto": "Código do Item",
        "data_compra": "Data da Compra",
        "codigo_fornecedor": "Fornecedor",
        "custo_unitario": "Custo Unitário",
        "quantidade": "Quantidade",
        "custo_total": "Custo Total"
    }

    for celula in ws[1]:

        if celula.value in cabecalhos:
            celula.value = cabecalhos[celula.value]

    for row in ws.iter_rows(min_row=2):

        # Data
        row[1].number_format = 'dd/mm/yyyy'

        # Custo Unitário
        row[3].number_format = '#,##0.0000'

        # Quantidade
        row[4].number_format = '#,##0'

        # Custo Total
        row[5].number_format = '#,##0.00'





def run(arquivo_excel):

    wb = load_workbook(
        arquivo_excel
    )

    
    
    
    


    # ========================================================
    # RESUMO EXECUTIVO
    # ========================================================

    ws = wb["Resumo Executivo"]

    reconstruir_resumo(ws)
    
    if "Compras Mensais" in wb.sheetnames:
        formatar_compras_mensais(
            wb["Compras Mensais"]
        )

    if "Top Fornecedores" in wb.sheetnames:

        formatar_top_fornecedores(
            wb["Top Fornecedores"]
        )

    if "ABC Fornecedores" in wb.sheetnames:

        formatar_abc_fornecedores(
            wb["ABC Fornecedores"]
        )

    if "Top Produtos" in wb.sheetnames:

        formatar_top_produtos(
            wb["Top Produtos"]
        )


    if "Base Produtos" in wb.sheetnames:

        formatar_base_produtos(
            wb["Base Produtos"]
        )

    if "Top Oportunidades" in wb.sheetnames:
        
               

        formatar_top_savings(
            wb["Top Oportunidades"]
        )

    if "Oportunidades de Economia" in wb.sheetnames:

        formatar_saving_completo(
            wb["Oportunidades de Economia"]
        )



    if "Variação de Preços" in wb.sheetnames:

        formatar_inflacao(
            wb["Variação de Preços"]
        )

    if "ABC Produtos" in wb.sheetnames:

        formatar_abc_produtos(
            wb["ABC Produtos"]
        )

    if "Evolução Histórica" in wb.sheetnames:

        formatar_evolucao_historica(
            wb["Evolução Histórica"]
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

    if "ABC Fornecedores" in wb.sheetnames:

        colorir_coluna_abc(
            wb["ABC Fornecedores"]
        )

    if "ABC Produtos" in wb.sheetnames:

        colorir_coluna_abc(
            wb["ABC Produtos"]
        )

    # ========================================================
    # SAVING
    # ========================================================

    if "Oportunidades de Economia" in wb.sheetnames:

        colorir_status(
            wb["Oportunidades de Economia"]
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
