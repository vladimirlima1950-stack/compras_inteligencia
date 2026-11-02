from fastapi import FastAPI, Request
from pathlib import Path
import pandas as pd
import glob

import requests
import os

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
def processar_compras(request: Request):
    
    print("***** ENTREI EM PROCESSAR_COMPRAS *****", flush=True)

    email_cliente = request.query_params.get("email")
    nome_cliente = request.query_params.get("nome")
    
    
    if not email_cliente:

        return {
            "status": "erro",
            "mensagem": "Email do cliente não informado."
        }

    if not nome_cliente:

        return {
            "status": "erro",
            "mensagem": "Nome do cliente não informado."
        }

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

        print("========== DATAFRAME ==========")
        print(df)
        print("===============================")
        
        


        # --------------------------------
        # valida número mínimo de colunas
        # --------------------------------

        if len(df.columns) < 5:

           return retornar_erro(
                nome_cliente,
                email_cliente,
                nome_arquivo,
                "Arquivo possui menos de 5 colunas.",
                0,
                []
           )
                       
           
           
        # --------------------------------
        # cabeçalhos obrigatórios
        # --------------------------------

        cabecalhos = [
            str(c).strip()
            for c in df.columns
        ]

        if any(not str(c).strip() for c in cabecalhos):

            
            return retornar_erro(
                nome_cliente,
                email_cliente,
                nome_arquivo,
                "Existem colunas sem nome no cabeçalho.",
                0,
                []
            )
                    
            
            
            
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
        print("=== DATA NF ===")
        print(df["data_nf"])
        print("================")

        # --------------------------------
        # conversão quantidade
        # --------------------------------

        df["quantidade"] = (
            df["quantidade"]
            .apply(converter_numero)
        )
        
        

        print("=== COLUNA QUANTIDADE ===")
        print(df["quantidade"])
        print("========================")

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

            linhas_excel = [
                x + 2
                for x in linhas_data_invalida
            ]

            mensagem = (
                "Foram encontradas datas inválidas.\n"
                f"Linhas: {linhas_excel}"
            )

            
            return retornar_erro(
                nome_cliente,
                email_cliente,
                nome_arquivo,
                mensagem,
                len(linhas_excel),
                linhas_excel
            )
                    
        
        # --------------------------------
        # validação de quantidade inválida
        # --------------------------------

        linhas_quantidade_invalida = (
            df[df["quantidade"].isna()]
            .index
            .tolist()
        )


        print(
            "LINHAS_QUANTIDADE_INVALIDA:",
            linhas_quantidade_invalida
        )

        if linhas_quantidade_invalida:

            linhas_excel = [
                x + 2
                for x in linhas_quantidade_invalida
            ]

            mensagem = (
                "Foram encontradas quantidades inválidas.\n"
                f"Linhas: {linhas_excel}"
            )

            return retornar_erro(
                nome_cliente,
                email_cliente,
                nome_arquivo,
                mensagem,
                len(linhas_excel),
                linhas_excel
            )
                
        
        
        
        # --------------------------------
        # validação de custo inválido
        # --------------------------------

        linhas_custo_invalido = (
            df[df["custo_unitario"].isna()]
            .index
            .tolist()
        )

        if linhas_custo_invalido:

            linhas_excel = [
                x + 2
                for x in linhas_custo_invalido
            ]

            mensagem = (
                "Foram encontrados custos inválidos.\n"
                f"Linhas: {linhas_excel}"
            )

            return retornar_erro(
                nome_cliente,
                email_cliente,
                nome_arquivo,
                mensagem,
                len(linhas_excel),
                linhas_excel
            )
                
        
        
        
        
        # --------------------------------
        # quantidade <= 0
        # --------------------------------

        linhas_quantidade_zero = (
            df[df["quantidade"] <= 0]
            .index
            .tolist()
        )

        if linhas_quantidade_zero:

            linhas_excel = [
                x + 2
                for x in linhas_quantidade_zero
            ]

            mensagem = (
                "Existem quantidades menores ou iguais a zero.\n"
                f"Linhas: {linhas_excel}"
            )

            return retornar_erro(
                nome_cliente,
                email_cliente,
                nome_arquivo,
                mensagem,
                len(linhas_excel),
                linhas_excel
            )
                
        
        
        
        # --------------------------------
        # custo <= 0
        # --------------------------------

        linhas_custo_zero = (
            df[df["custo_unitario"] <= 0]
            .index
            .tolist()
        )

        if linhas_custo_zero:

            linhas_excel = [
                x + 2
                for x in linhas_custo_zero
            ]

            mensagem = (
                "Existem custos unitários menores ou iguais a zero.\n"
                f"Linhas: {linhas_excel}"
            )

            return retornar_erro(
                nome_cliente,
                email_cliente,
                nome_arquivo,
                mensagem,
                len(linhas_excel),
                linhas_excel
            )





        # --------------------------------
        # PROCESSAMENTO VALIDADO
        # --------------------------------

        return {

            "status": "ok",
            
            "mensagem":
                "Arquivo validado com sucesso.",

            "sistema":
                "compras_inteligencia",

            "arquivo":
                nome_arquivo,

            "linhas":
                int(len(df)),

            "colunas":
                int(len(df.columns)),

            "cabecalhos_origem":
                cabecalhos_origem,

            "nomes_colunas": [
                "codigo_produto",
                "codigo_fornecedor",
                "data_nf",
                "quantidade",
                "custo_unitario"
            ]
        }


        

    except Exception as e:

        return {
             "status": "erro",
             "mensagem": str(e)
        }




        
def enviar_email_erro(
    nome_cliente,
    email_destino,
    nome_arquivo,
    mensagem_erro
):
    
    print("***** ENTREI EM ENVIAR_EMAIL_ERRO *****", flush=True)

    api_key = os.getenv("RESEND_API_KEY")

    if not api_key:

        print("RESEND_API_KEY não encontrada.")
        return

    html_body = f"""
    <h2>Processamento interrompido</h2>

    <p>Olá, {nome_cliente}.</p>

    <p>
    O arquivo <b>{nome_arquivo}</b> não pôde ser processado pelo sistema
    Compras Inteligência.
    </p>

    <p>
    Motivo:
    </p>

    <pre>
{mensagem_erro}
    </pre>

    <p>
    Arquivo analisado:
    <b>{nome_arquivo}</b>
    </p>

    <p>
    Corrija os dados da planilha e realize um novo envio.
    </p>

    <p>
    Atenciosamente<br>
    MUPE Consultoria
    </p>
    """

    payload = {
        "from": "MUPE Consultoria <vladimir.lima@mupeconsult.com>",
        "to": [email_destino],
        "subject": "Erro no processamento do Compras Inteligência",
        "html": html_body
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    

       
     try:

        r = requests.post(
            "https://api.resend.com/emails",
            json=payload,
            headers=headers,
            timeout=30
        )

        print("RESEND STATUS:", r.status_code)
        print("RESEND RESPOSTA:", r.text)

        r.raise_for_status()

        print("EMAIL ENVIADO COM SUCESSO.")

    except Exception as e:

        print("ERRO NO ENVIO DO EMAIL:", str(e))
       
       
       
       
        
def retornar_erro(
    nome_cliente,
    email_cliente,
    nome_arquivo,
    mensagem,
    quantidade,
    linhas
):

    print("***** ENTREI EM RETORNAR_ERRO *****", flush=True)

    if email_cliente:

        enviar_email_erro(
            nome_cliente=nome_cliente or "Cliente",
            email_destino=email_cliente,
            nome_arquivo=nome_arquivo,
            mensagem_erro=mensagem
        )



    return {
        "status": "erro",
        "mensagem": mensagem,
        "quantidade_erros": quantidade,
        "linhas": linhas
    }

 