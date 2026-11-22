# compras_330_envio_email.py

# ============================================================
# ENVIO DE E-MAIL DO COMPRAS INTELIGENCIA
# ============================================================

import os
import base64
import requests


def run(
        arquivo_xlsx: str,
        email_destino: str,
        nome: str = "Cliente",
        idioma: str = "PT"
        
):

    print(
        f"Enviando relatório para "
        f"{email_destino}"
    )

    RESEND_API_KEY = os.getenv(
        "RESEND_API_KEY"
    )

    if not RESEND_API_KEY:

        print(
            "ERRO: RESEND_API_KEY "
            "não configurada."
        )

        return False

    if not os.path.exists(
        arquivo_xlsx
    ):

        print(
            f"Arquivo não encontrado: "
            f"{arquivo_xlsx}"
        )

        return False

    with open(
        arquivo_xlsx,
        "rb"
    ) as f:

        arquivo_bytes = f.read()

    arquivo_base64 = (
        base64
        .b64encode(
            arquivo_bytes
        )
        .decode("utf-8")
    )

    primeiro_nome = (
        nome.split()[0]
        if nome
        else "Cliente"
    )

    if idioma.upper() == "EN":

        saudacao = f"Hello, {primeiro_nome}!"

        introducao = (
            "The Purchasing Intelligence report "
            "has been successfully processed "
            "and is ready for analysis."
        )

    else:

        saudacao = f"Olá, {primeiro_nome}!"

        introducao = (
            "O relatório do módulo "
            "Compras Inteligência foi processado "
            "com sucesso e já está disponível para análise."
        )



    if idioma.upper() == "EN":

        assunto = (
            "Purchasing Intelligence - "
            "Report Available"
        )

    else:

        assunto = (
            "Compras Inteligência - "
            "Relatório Disponível"
        )



    if idioma.upper() == "EN":

        planilha = (
            "The attached Excel workbook contains "
            "the main indicators, analyses and opportunities "
            "identified during the evaluated period."
        )

        conteudo_relatorio = (
            "The report contains:"
        )

        historico = (
            "The Historical Evolution worksheet presents the chronological purchasing history by item, allowing analysis of supplier evolution, unit cost evolution, purchased quantities and total amounts throughout the evaluated period."
        )



    else:

        planilha = (
            "A planilha Excel segue anexada contendo "
            "os principais indicadores, análises e oportunidades "
            "identificadas no período avaliado."
        )

        conteudo_relatorio = (
            "O relatório contém:"
        )

        historico = (
            "A aba Evolução Histórica apresenta o histórico cronológico das compras por item, permitindo analisar a evolução dos fornecedores, dos custos unitários, das quantidades adquiridas e dos valores totais comprados ao longo do período avaliado."
        )


    if idioma.upper() == "EN":

        texto_anomalia = (
            "Some opportunities classified as "
            "ANOMALY may result from:"
        )

    else:

        texto_anomalia = (
            "Algumas oportunidades classificadas "
            "como ANOMALIA podem decorrer de:"
        )



    if idioma.upper() == "EN":

        aba_1 = "Executive Summary"
        aba_2 = "Monthly Purchases"
        aba_3 = "Top Suppliers"
        aba_4 = "ABC Suppliers"
        aba_5 = "Top Products"
        aba_6 = "Product Database"
        aba_7 = "ABC Products"
        aba_8 = "Top Opportunities"
        aba_9 = "Savings Opportunities"
        aba_10 = "Price Variation"
        aba_11 = "Historical Evolution"

    else:

        aba_1 = "Resumo Executivo"
        aba_2 = "Compras Mensais"
        aba_3 = "Top Fornecedores"
        aba_4 = "ABC Fornecedores"
        aba_5 = "Top Produtos"
        aba_6 = "Base Produtos"
        aba_7 = "ABC Produtos"
        aba_8 = "Top Oportunidades"
        aba_9 = "Oportunidades de Economia"
        aba_10 = "Variação de Preços"
        aba_11 = "Evolução Histórica"



    payload = {

        "from":
        "MUPE Consultoria "
        "<noreply@mupeconsult.com>",

        "to":
        email_destino,

        "subject":
        assunto,

        "html": f"""

        <p style='font-family:Arial;
                  font-size:15px;
                  color:#333;'>

            {saudacao}

        </p>

        <p style='font-family:Arial;
                  font-size:15px;
                  color:#333;'>

            {introducao}

        </p>

        <p style='font-family:Arial;
                  font-size:15px;
                  color:#333;'>

            {planilha}

        </p>

        <p style='font-family:Arial;
                  font-size:15px;
                  color:#333;'>

            {conteudo_relatorio}

        </p>

        <ul style='font-family:Arial;
                   font-size:15px;
                   color:#333;'>

            <li>{aba_1}</li>

            <li>{aba_2}</li>

            <li>{aba_3}</li>

            <li>{aba_4}</li>

            <li>{aba_5}</li>

            <li>{aba_6}</li>
            
            <li>{aba_7}</li>

            <li>{aba_8}</li>

            <li>{aba_9}</li>

            <li>{aba_10}</li>

            <li>{aba_11}</li>
            
            

        </ul>
        
        <ul>
        {historico}
        
        </ul>
        

        <p style='font-family:Arial;
                  font-size:15px;
                  color:#333;'>

            {texto_anomalia}

        </p>

        <ul style='font-family:Arial;
                   font-size:15px;
                   color:#333;'>

            <li>Diferenças de unidade de medida</li>

            <li>Diferenças de embalagem</li>

            <li>Condições comerciais específicas</li>

            <li>Compras promocionais</li>

            <li>Possíveis inconsistências cadastrais</li>

        </ul>

        <p style='font-family:Arial;
                  font-size:15px;
                  color:#333;'>

            Recomendamos avaliar cada
            oportunidade antes de tomar
            decisões de negociação.

        </p>

        <p style='font-family:Arial;
                  font-size:15px;
                  color:#333;'>

            Atenciosamente,

        </p>

        <p style='font-family:Arial;
                  font-size:15px;
                  color:#333;'>

            MUPE Consultoria<br>

            Vladimir de Lima<br>

            WhatsApp
            (19) 99783-5054

        </p>

        """,

        "attachments": [

            {

                "filename":
                os.path.basename(
                    arquivo_xlsx
                ),

                "content":
                arquivo_base64,

                "type":
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            }

        ]

    }

    response = requests.post(

        "https://api.resend.com/emails",

        headers={

            "Authorization":
            f"Bearer {RESEND_API_KEY}",

            "Content-Type":
            "application/json"

        },

        json=payload

    )

    if 200 <= response.status_code < 300:

        print(
            "E-mail enviado "
            "com sucesso."
        )

        return True

    else:

        print(
            f"Erro ao enviar e-mail: "
            f"{response.text}"
        )

        return False