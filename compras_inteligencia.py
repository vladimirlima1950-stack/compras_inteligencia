from fastapi import FastAPI
from pathlib import Path
import pandas as pd
import glob

app = FastAPI(
    title="Compras Inteligência"
)

UPLOAD_DIR = "uploads"


# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():

    return {
        "sistema": "compras_inteligencia",
        "status": "online"
    }


# =====================================================
# CONVERSAO NUMERICA
# SUPORTA BR E EUA
# =====================================================

def converter_numero(valor):

    if pd.isna(valor):
        return None

    valor = str(valor).strip()

    if valor == "":
        return None

    try:

        # Ex:
        # BR  -> 1.234,56
        # EUA -> 1,234.56

        if "," in valor and "." in valor:

            if valor.rfind(",") > valor.rfind("."):

                # formato brasileiro
                valor = valor.replace(".", "")
                valor = valor.replace(",", ".")

            else:

                # formato americano
                valor = valor.replace(",", "")

        elif "," in valor:

            # assume decimal brasileiro
            valor = valor.replace(".", "")
            valor = valor.replace(",", ".")

        return float(valor)

    except Exception:
        return None


# =====================================================
# CONVERSAO DE DATAS
# SUPORTA:
# DD/MM/AAAA
# DD-MM-AAAA
# YYYY-MM-DD
# YYYY/MM/DD
# DATAS EXCEL
# =====================================================

def converter_data(coluna):

    resultado = pd.to_datetime(
        coluna,
        dayfirst=True,
        errors="coerce"
    )

    mascara = resultado.isna()

    if mascara.any():

        resultado.loc[mascara] = pd.to_datetime(
            coluna.loc[mascara],
            yearfirst=True,
            errors="coerce"
        )

    return resultado


# =====================================================
# LEITURA DE ARQUIVOS
# CSV / XLS / XLSX
# =====================================================

def carregar_arquivo(caminho):

    extensao = Path(caminho).suffix.lower()

    if extensao == ".csv":

        df = pd.read_csv(
            caminho,
            sep=None,
            engine="python"
        )

    elif extensao == ".xlsx":

        df = pd.read_excel(
            caminho,
            engine="openpyxl"
        )

    elif extensao == ".xls":

        df = pd.read_excel(
            caminho,
            engine="xlrd"
        )

    else:

        raise Exception(
            f"Formato não suportado: {extensao}"
        )

    return df


# =====================================================
# LOCALIZA ULTIMO ARQUIVO
# =====================================================

def obter_ultimo_arquivo():

    arquivos = []

    arquivos.extend(
        glob.glob(f"{UPLOAD_DIR}/*.csv")
    )

    arquivos.extend(
        glob.glob(f"{UPLOAD_DIR}/*.xls")
    )

    arquivos.extend(
        glob.glob(f"{UPLOAD_DIR}/*.xlsx")
    )

    if not arquivos:
        return None

    return max(
        arquivos,
        key=lambda x: Path(x).stat().st_mtime
    )


# =====================================================
# PROCESSAMENTO
# =====================================================

@app.get("/processar_compras")
def processar_compras():

    caminho = obter_ultimo_arquivo()

    if not caminho:

        return {
            "status": "erro",
            "mensagem": (
                "Nenhum arquivo encontrado "
                "na pasta uploads."
            )
        }

    try:

        nome_arquivo = Path(caminho).name

        df = carregar_arquivo(caminho)

        # --------------------------------
        # valida número mínimo de colunas
        # --------------------------------

        if len(df.columns) < 5:

            return {
                "status": "erro",
                "mensagem": (
                    "Arquivo inválido. "
                    "São necessárias pelo menos "
                    "5 colunas."
                )
            }

        # --------------------------------
        # cabeçalhos obrigatórios
        # --------------------------------

        cabecalhos = [
            str(c).strip()
            for c in df.columns
        ]

        if any(c == "" for c in cabecalhos):

            return {
                "status": "erro",
                "mensagem": (
                    "Existem colunas sem nome "
                    "no cabeçalho."
                )
            }

        # --------------------------------
        # usa apenas as 5 primeiras colunas
        # --------------------------------

        df = df.iloc[:, :5]

        cabecalhos_origem = list(df.columns)

        # --------------------------------
        # nomes internos padronizados
        # --------------------------------

        df.columns = [
            "codigo_produto",
            "codigo_fornecedor",
            "data_nf",
            "quantidade",
            "custo_unitario"
        ]

        # --------------------------------
        # conversão data
        # --------------------------------

        df["data_nf"] = converter_data(
            df["data_nf"]
        )

        # --------------------------------
        # conversão quantidade
        # --------------------------------

        df["quantidade"] = (
            df["quantidade"]
            .apply(converter_numero)
        )

        # --------------------------------
        # conversão custo unitário
        # --------------------------------

        df["custo_unitario"] = (
            df["custo_unitario"]
            .apply(converter_numero)
        )

        # --------------------------------
        # estatísticas
        # --------------------------------

        # --------------------------------
        # validação de datas
        # --------------------------------

        linhas_data_invalida = (
            df[df["data_nf"].isna()]
            .index
            .tolist()
        )

        if linhas_data_invalida:

            return {
                "status": "erro",
                "mensagem":
                    "Foram encontradas datas inválidas.",
                "quantidade_erros":
                    len(linhas_data_invalida),
                "linhas":
                    [x + 2 for x in linhas_data_invalida]
            }

        # --------------------------------
        # validação de quantidade inválida
        # --------------------------------

        linhas_quantidade_invalida = (
            df[df["quantidade"].isna()]
            .index
            .tolist()
        )

        if linhas_quantidade_invalida:

            return {
                "status": "erro",
                "mensagem":
                    "Foram encontradas quantidades inválidas.",
                "quantidade_erros":
                    len(linhas_quantidade_invalida),
                "linhas":
                    [x + 2 for x in linhas_quantidade_invalida]
            }

        # --------------------------------
        # validação de custo inválido
        # --------------------------------

        linhas_custo_invalido = (
            df[df["custo_unitario"].isna()]
            .index
            .tolist()
        )

        if linhas_custo_invalido:

            return {
                "status": "erro",
                "mensagem":
                    "Foram encontrados custos inválidos.",
                "quantidade_erros":
                    len(linhas_custo_invalido),
                "linhas":
                    [x + 2 for x in linhas_custo_invalido]
            }

        # --------------------------------
        # quantidade <= 0
        # --------------------------------

        linhas_quantidade_zero = (
            df[df["quantidade"] <= 0]
            .index
            .tolist()
        )

        if linhas_quantidade_zero:

            return {
                "status": "erro",
                "mensagem":
                    "Existem quantidades menores ou iguais a zero.",
                "quantidade_erros":
                    len(linhas_quantidade_zero),
                "linhas":
                    [x + 2 for x in linhas_quantidade_zero]
            }

        # --------------------------------
        # custo <= 0
        # --------------------------------

        linhas_custo_zero = (
            df[df["custo_unitario"] <= 0]
            .index
            .tolist()
        )

        if linhas_custo_zero:

            return {
                "status": "erro",
                "mensagem":
                    "Existem custos unitários menores ou iguais a zero.",
                "quantidade_erros":
                    len(linhas_custo_zero),
                "linhas":
                    [x + 2 for x in linhas_custo_zero]
            }