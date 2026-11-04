
# compras_310_formatacao_excel.py

# ============================================================
# COMPRAS INTELIGENCIA
# FORMATACAO EXCEL
# ============================================================

from openpyxl import load_workbook

from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment
)

# ============================================================
# CORES
# ============================================================

COR_CABECALHO = "1F4E78"

COR_VERDE = "92D050"
COR_AMARELO = "FFD966"
COR_VERMELHO = "FF9999"

COR_ZEBRA = "F2F2F2"

# ============================================================
# CABECALHOS AMIGAVEIS
# ============================================================

MAPA_CABECALHOS = {

    "codigo_produto":
        "Produto",

    "codigo_fornecedor":
        "Fornecedor",

    "valor_comprado":
        "Valor Comprado",

    "percentual":
        "Participação (%)",

    "percentual_acumulado":
        "Acumulado (%)",

    "classe":
        "Classe ABC",

    "saving_absoluto":
        "Saving",

    "saving_percentual":
        "Saving (%)",

    "ultimo_mes":
        "Última Compra",

    "custo_atual":
        "Custo Atual",

    "menor_custo_historico":
        "Menor Custo Histórico"

}

# ============================================================
# FORMATACAO CABECALHO
# ============================================================

def formatar_cabecalho(ws):

    azul = PatternFill(
        "solid",
        fgColor=COR_CABECALHO
    )

    fonte = Font(
        color="FFFFFF",
        bold=True
    )

    for cell in wscell.fill = azul
        cell.font = fonte

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

# ============================================================
# AJUSTE COLUNAS
# ============================================================

def ajustar_largura(ws):

    for coluna in ws.columns:

        largura = 0

        letra = coluna[0].column_letter

        for celula in coluna:

            try:

                if celula.value is not None:

                    largura = max(
                        largura,
                        len(str(celula.value))
                    )

            except:
                pass

        ws.column_dimensions[
            letra
        ].width = largura + 3

# ============================================================
# CABECALHOS AMIGAVEIS
# ============================================================

def renomear_cabecalhos(ws):

    for cell in ws[1]:

        if cell.value in MAPA_CABECALHOS:

            cell.value = MAPA_CABECALHOS[
                cell.value
            ]

# ============================================================
# FORMATO NUMEROS
# ============================================================

def formatar_numeros(ws):

    colunas_monetarias = {

        "Valor Comprado",
        "Valor",
        "Saving",
        "Custo Atual",
        "Menor Custo Histórico"
    }

    cabecalhos = [
        c.value for c in ws[1]
    ]

    for idx, nome in enumerate(
        cabecalhos,
        start=1
    ):

        if nome in colunas_monetarias:

            for linha in range(
                2,
                ws.max_row + 1
            ):

                celula = ws.cell(
                    linha,
                    idx
                )

                if isinstance(
                    celula.value,
                    (int, float)
                ):

                    celula.number_format = (
                        '#,##0.00'
                    )

# ============================================================
# FORMATO PERCENTUAIS
# ============================================================

def formatar_percentuais(ws):

    cabecalhos = [
        c.value for c in ws[1]
    ]

    for idx, nome in enumerate(
        cabecalhos,
        start=1
    ):

        if nome in {

            "Participação (%)",
            "Acumulado (%)",
            "Saving (%)"

        }:

            for linha in range(
                2,
                ws.max_row + 1
            ):

                celula = ws.cell(
                    linha,
                    idx
                )

                if isinstance(
                    celula.value,
                    (int, float)
                ):

                    celula.value = (
                        celula.value / 100
                    )

                    celula.number_format = (
                        "0.00%"
                    )

# ============================================================
# ZEBRA
# ============================================================

def aplicar_zebra(ws):

    cinza = PatternFill(
        "solid",
        fgColor=COR_ZEBRA
    )

    for linha in range(
        2,
        ws.max_row + 1
    ):

        if linha % 2 == 0:

            for cell in ws[linha]:

                if not cell.fill.fill_type:

                    cell.fill = cinza

# ============================================================
# CLASSE ABC
# ============================================================

def colorir_coluna_abc(ws):

    for row in ws.iter_rows(
        min_row=2
    ):

        for cell in row:

            if cell.value == "A":

                cell.fill = PatternFill(
                    "solid",
                    fgColor=COR_VERDE
                )

            elif cell.value == "B":

                cell.fill = PatternFill(
                    "solid",
                    fgColor=COR_AMARELO
                )

            elif cell.value == "C":

                cell.fill = PatternFill(
                    "solid",
                    fgColor=COR_VERMELHO
                )

# ============================================================
# STATUS SAVING
# ============================================================

def colorir_status(ws):

    for row in ws.iter_rows(
        min_row=2
    ):

        for cell in row:

            if cell.value == "NORMAL":

                cell.fill = PatternFill(
                    "solid",
                    fgColor=COR_VERDE
                )

            elif cell.value == "ATENCAO":

                cell.fill = PatternFill(
                    "solid",
                    fgColor=COR_AMARELO
                )

            elif cell.value == "ANOMALIA":

                cell.fill = PatternFill(
                    "solid",
                    fgColor=COR_VERMELHO
                )

# ============================================================
# ACAO SAVING
# ============================================================

def adicionar_coluna_acao(ws):

    headers = [
        c.value
        for c in ws[1]
    ]

    if "status" not in headers:
        return

    status_col = (
        headers.index("status") + 1
    )

    nova_col = ws.max_column + 1

    ws.cell(
        1,
        nova_col,
        "AÇÃO"
    )

    for linha in range(
        2,
        ws.max_row + 1
    ):

        status = ws.cell(
            linha,
            status_col
        ).value

        if status == "ANOMALIA":

            acao = "VALIDAR"

        elif status == "ATENCAO":

            acao = "INVESTIGAR"

        else:

            acao = "NEGOCIAR"

        ws.cell(
            linha,
            nova_col,
            acao
        )

# ============================================================
# RESUMO EXECUTIVO
# ============================================================

def reconstruir_resumo(ws):

    if ws.max_row < 2:
        return

    dados = {}

    cabecalhos = [
        c.value for c in ws[1]
    ]

    valores = [
        c.value for c in ws[2]
    ]

    for k, v in zip(
        cabecalhos,
        valores
    ):
        dados[k] = v

    ws.delete_rows(
        1,
        ws.max_row
    )

    ws["A1"] = "Indicador"
    ws["B1"] = "Valor"

    linha = 2

    indicadores = [

        ("Valor Total Comprado",
         dados.get("valor_total_comprado")),

        ("Quantidade Comprada",
         dados.get("quantidade_total_comprada")),

        ("Produtos Distintos",
         dados.get("produtos_distintos")),

        ("Fornecedores Distintos",
         dados.get("fornecedores_distintos")),

        ("Meses Avaliados",
         dados.get("meses_periodo")),

        ("Compra Média Mensal",
         dados.get("compra_media_mensal")),

        ("Maior Mês",
         dados.get("maior_mes_compra")),

        ("Valor do Maior Mês",
         dados.get("valor_maior_mes")),

        ("Menor Mês",
         dados.get("menor_mes_compra")),

        ("Valor do Menor Mês",
         dados.get("valor_menor_mes")),

        ("Oportunidades Totais",
         dados.get("oportunidades_totais")),

        ("Oportunidades Normais",
         dados.get("qtd_normal")),

        ("Oportunidades Atenção",
         dados.get("qtd_atencao")),

        ("Oportunidades Anomalia",
         dados.get("qtd_anomalia")),

        ("Saving Total",
         dados.get("saving_total")),

        ("Saving Médio",
         dados.get("saving_medio")),

        ("Maior Saving",
         dados.get("maior_saving")),

        ("Maior Saving Normal",
         dados.get("maior_saving_normal")),

        ("Maior Saving Atenção",
         dados.get("maior_saving_atencao")),

        ("Maior Saving Anomalia",
         dados.get("maior_saving_anomalia")),

        ("Inflação Média",
         dados.get("inflacao_media_periodo"))

    ]

    for indicador, valor in indicadores:

        ws.cell(linha, 1, indicador)
        ws.cell(linha, 2, valor)

        linha += 1

# ============================================================
# EXECUCAO
# ============================================================

def run(arquivo_excel):

    wb = load_workbook(
        arquivo_excel
    )

    if "Resumo Executivo" in wb.sheetnames:

        reconstruir_resumo(
            wb["Resumo Executivo"]
        )

    for ws in wb.worksheets:

        renomear_cabecalhos(ws)

        formatar_cabecalho(ws)

        formatar_numeros(ws)

        formatar_percentuais(ws)

        aplicar_zebra(ws)

        ws.freeze_panes = "A2"

        ws.auto_filter.ref = (
            ws.dimensions
        )

        ajustar_largura(ws)

    if "ABC Fornecedores" in wb.sheetnames:

        colorir_coluna_abc(
            wb["ABC Fornecedores"]
        )

    if "ABC Produtos" in wb.sheetnames:

        colorir_coluna_abc(
            wb["ABC Produtos"]
        )

    for nome in [

        "Top Savings",
        "Saving Completo"

    ]:

        if nome in wb.sheetnames:

            adicionar_coluna_acao(
                wb[nome]
            )

            colorir_status(
                wb[nome]
            )

    wb.save(
        arquivo_excel
    )

    print(
        "Excel formatado com sucesso."
    )

    return arquivo_excel


# compras_310_formatacao_excel.py

# ============================================================
# COMPRAS INTELIGENCIA
# FORMATACAO EXCEL
# ============================================================

from openpyxl import load_workbook

from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment
)

# ============================================================
# CORES
# ============================================================

COR_CABECALHO = "1F4E78"

COR_VERDE = "92D050"
COR_AMARELO = "FFD966"
COR_VERMELHO = "FF9999"

COR_ZEBRA = "F2F2F2"

# ============================================================
# CABECALHOS AMIGAVEIS
# ============================================================

MAPA_CABECALHOS = {

    "codigo_produto":
        "Produto",

    "codigo_fornecedor":
        "Fornecedor",

    "valor_comprado":
        "Valor Comprado",

    "percentual":
        "Participação (%)",

    "percentual_acumulado":
        "Acumulado (%)",

    "classe":
        "Classe ABC",

    "saving_absoluto":
        "Saving",

    "saving_percentual":
        "Saving (%)",

    "ultimo_mes":
        "Última Compra",

    "custo_atual":
        "Custo Atual",

    "menor_custo_historico":
        "Menor Custo Histórico"

}

# ============================================================
# FORMATACAO CABECALHO
# ============================================================

def formatar_cabecalho(ws):

    azul = PatternFill(
        "solid",
        fgColor=COR_CABECALHO
    )

    fonte = Font(
        color="FFFFFF",
        bold=True
    )

    for cell in wscell.fill = azul
        cell.font = fonte

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

# ============================================================
# AJUSTE COLUNAS
# ============================================================

def ajustar_largura(ws):

    for coluna in ws.columns:

        largura = 0

        letra = coluna[0].column_letter

        for celula in coluna:

            try:

                if celula.value is not None:

                    largura = max(
                        largura,
                        len(str(celula.value))
                    )

            except:
                pass

        ws.column_dimensions[
            letra
        ].width = largura + 3

# ============================================================
# CABECALHOS AMIGAVEIS
# ============================================================

def renomear_cabecalhos(ws):

    for cell in ws[1]:

        if cell.value in MAPA_CABECALHOS:

            cell.value = MAPA_CABECALHOS[
                cell.value
            ]

# ============================================================
# FORMATO NUMEROS
# ============================================================

def formatar_numeros(ws):

    colunas_monetarias = {

        "Valor Comprado",
        "Valor",
        "Saving",
        "Custo Atual",
        "Menor Custo Histórico"
    }

    cabecalhos = [
        c.value for c in ws[1]
    ]

    for idx, nome in enumerate(
        cabecalhos,
        start=1
    ):

        if nome in colunas_monetarias:

            for linha in range(
                2,
                ws.max_row + 1
            ):

                celula = ws.cell(
                    linha,
                    idx
                )

                if isinstance(
                    celula.value,
                    (int, float)
                ):

                    celula.number_format = (
                        '#,##0.00'
                    )

# ============================================================
# FORMATO PERCENTUAIS
# ============================================================

def formatar_percentuais(ws):

    cabecalhos = [
        c.value for c in ws[1]
    ]

    for idx, nome in enumerate(
        cabecalhos,
        start=1
    ):

        if nome in {

            "Participação (%)",
            "Acumulado (%)",
            "Saving (%)"

        }:

            for linha in range(
                2,
                ws.max_row + 1
            ):

                celula = ws.cell(
                    linha,
                    idx
                )

                if isinstance(
                    celula.value,
                    (int, float)
                ):

                    celula.value = (
                        celula.value / 100
                    )

                    celula.number_format = (
                        "0.00%"
                    )

# ============================================================
# ZEBRA
# ============================================================

def aplicar_zebra(ws):

    cinza = PatternFill(
        "solid",
        fgColor=COR_ZEBRA
    )

    for linha in range(
        2,
        ws.max_row + 1
    ):

        if linha % 2 == 0:

            for cell in ws[linha]:

                if not cell.fill.fill_type:

                    cell.fill = cinza

# ============================================================
# CLASSE ABC
# ============================================================

def colorir_coluna_abc(ws):

    for row in ws.iter_rows(
        min_row=2
    ):

        for cell in row:

            if cell.value == "A":

                cell.fill = PatternFill(
                    "solid",
                    fgColor=COR_VERDE
                )

            elif cell.value == "B":

                cell.fill = PatternFill(
                    "solid",
                    fgColor=COR_AMARELO
                )

            elif cell.value == "C":

                cell.fill = PatternFill(
                    "solid",
                    fgColor=COR_VERMELHO
                )

# ============================================================
# STATUS SAVING
# ============================================================

def colorir_status(ws):

    for row in ws.iter_rows(
        min_row=2
    ):

        for cell in row:

            if cell.value == "NORMAL":

                cell.fill = PatternFill(
                    "solid",
                    fgColor=COR_VERDE
                )

            elif cell.value == "ATENCAO":

                cell.fill = PatternFill(
                    "solid",
                    fgColor=COR_AMARELO
                )

            elif cell.value == "ANOMALIA":

                cell.fill = PatternFill(
                    "solid",
                    fgColor=COR_VERMELHO
                )

# ============================================================
# ACAO SAVING
# ============================================================

def adicionar_coluna_acao(ws):

    headers = [
        c.value
        for c in ws[1]
    ]

    if "status" not in headers:
        return

    status_col = (
        headers.index("status") + 1
    )

    nova_col = ws.max_column + 1

    ws.cell(
        1,
        nova_col,
        "AÇÃO"
    )

    for linha in range(
        2,
        ws.max_row + 1
    ):

        status = ws.cell(
            linha,
            status_col
        ).value

        if status == "ANOMALIA":

            acao = "VALIDAR"

        elif status == "ATENCAO":

            acao = "INVESTIGAR"

        else:

            acao = "NEGOCIAR"

        ws.cell(
            linha,
            nova_col,
            acao
        )

# ============================================================
# RESUMO EXECUTIVO
# ============================================================

def reconstruir_resumo(ws):

    if ws.max_row < 2:
        return

    dados = {}

    cabecalhos = [
        c.value for c in ws[1]
    ]

    valores = [
        c.value for c in ws[2]
    ]

    for k, v in zip(
        cabecalhos,
        valores
    ):
        dados[k] = v

    ws.delete_rows(
        1,
        ws.max_row
    )

    ws["A1"] = "Indicador"
    ws["B1"] = "Valor"

    linha = 2

    indicadores = [

        ("Valor Total Comprado",
         dados.get("valor_total_comprado")),

        ("Quantidade Comprada",
         dados.get("quantidade_total_comprada")),

        ("Produtos Distintos",
         dados.get("produtos_distintos")),

        ("Fornecedores Distintos",
         dados.get("fornecedores_distintos")),

        ("Meses Avaliados",
         dados.get("meses_periodo")),

        ("Compra Média Mensal",
         dados.get("compra_media_mensal")),

        ("Maior Mês",
         dados.get("maior_mes_compra")),

        ("Valor do Maior Mês",
         dados.get("valor_maior_mes")),

        ("Menor Mês",
         dados.get("menor_mes_compra")),

        ("Valor do Menor Mês",
         dados.get("valor_menor_mes")),

        ("Oportunidades Totais",
         dados.get("oportunidades_totais")),

        ("Oportunidades Normais",
         dados.get("qtd_normal")),

        ("Oportunidades Atenção",
         dados.get("qtd_atencao")),

        ("Oportunidades Anomalia",
         dados.get("qtd_anomalia")),

        ("Saving Total",
         dados.get("saving_total")),

        ("Saving Médio",
         dados.get("saving_medio")),

        ("Maior Saving",
         dados.get("maior_saving")),

        ("Maior Saving Normal",
         dados.get("maior_saving_normal")),

        ("Maior Saving Atenção",
         dados.get("maior_saving_atencao")),

        ("Maior Saving Anomalia",
         dados.get("maior_saving_anomalia")),

        ("Inflação Média",
         dados.get("inflacao_media_periodo"))

    ]

    for indicador, valor in indicadores:

        ws.cell(linha, 1, indicador)
        ws.cell(linha, 2, valor)

        linha += 1

# ============================================================
# EXECUCAO
# ============================================================

def run(arquivo_excel):

    wb = load_workbook(
        arquivo_excel
    )

    if "Resumo Executivo" in wb.sheetnames:

        reconstruir_resumo(
            wb["Resumo Executivo"]
        )

    for ws in wb.worksheets:

        renomear_cabecalhos(ws)

        formatar_cabecalho(ws)

        formatar_numeros(ws)

        formatar_percentuais(ws)

        aplicar_zebra(ws)

        ws.freeze_panes = "A2"

        ws.auto_filter.ref = (
            ws.dimensions
        )

        ajustar_largura(ws)

    if "ABC Fornecedores" in wb.sheetnames:

        colorir_coluna_abc(
            wb["ABC Fornecedores"]
        )

    if "ABC Produtos" in wb.sheetnames:

        colorir_coluna_abc(
            wb["ABC Produtos"]
        )

    for nome in [

        "Top Savings",
        "Saving Completo"

    ]:

        if nome in wb.sheetnames:

            adicionar_coluna_acao(
                wb[nome]
            )

            colorir_status(
                wb[nome]
            )

    wb.save(
        arquivo_excel
    )

    print(
        "Excel formatado com sucesso."
    )

    return arquivo_excel
