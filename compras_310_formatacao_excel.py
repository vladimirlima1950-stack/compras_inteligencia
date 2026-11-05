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

        ("Saving Total",
         dados["saving_total"]),

        ("Saving Médio",
         dados["saving_medio"]),

        ("Maior Saving",
         dados["maior_saving"]),

        ("Maior Saving Normal",
         dados["maior_saving_normal"]),

        ("Maior Saving Atenção",
         dados["maior_saving_atencao"]),

        ("Maior Saving Anomalia",
         dados["maior_saving_anomalia"]),

        ("Inflação Média",
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

    formatar_cabecalho(w


def formatar_valores_resumo(ws):

    indicadores_2_casas = {
        "Valor Total Comprado",
        "Quantidade Comprada",
        "Compra Média Mensal",
        "Valor do Maior Mês",
        "Valor do Menor Mês",
        "Saving Total",
        "Saving Médio",
        "Maior Saving",
        "Maior Saving Normal",
        "Maior Saving Atenção",
        "Maior Saving Anomalia",
        "Inflação Média"
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


def run(arquivo_excel):

    wb = load_workbook(
        arquivo_excel
    )

    # ========================================================
    # RESUMO EXECUTIVO
    # ========================================================

    ws = wb["Resumo Executivo"]

    reconstruir_resumo(ws)

    # ========================================================
    # TODAS AS ABAS
    # ========================================================

    for ws in wb.worksheets:

        ws.freeze_panes = "A2"

        ws.auto_filter.ref = (
            ws.dimensions
        )

        formatar_cabecalho(ws)
        formatar_valores_resumo(ws)

        ajustar_largura(ws)

    # ========================================================
    # ABC
    # ========================================================

    if "ABC Fornec" in wb.sheetnames:

        colorir_coluna_abc(
            wb["ABC Fornec"]
        )

    if "ABC Produtos" in wb.sheetnames:

        colorir_coluna_abc(
            wb["ABC Produtos"]
        )

    # ========================================================
    # SAVING
    # ========================================================

    if "Saving" in wb.sheetnames:

        colorir_status(
            wb["Saving"]
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
