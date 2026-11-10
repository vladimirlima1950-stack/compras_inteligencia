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
        nome: str = "Cliente"
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

    payload = {

        "from":
        "MUPE Consultoria "
        "<noreply@mupeconsult.com>",

        "to":
        email_destino,

        "subject":
        "Compras Inteligência - "
        "Relatório Disponível",

        "html": f"""

        <p style='font-family:Arial;
                  font-size:15px;
                  color:#333;'>

            Olá, {primeiro_nome}!

        </p>

        <p style='font-family:Arial;
                  font-size:15px;
                  color:#333;'>

            O relatório do módulo
            <strong>
            Compras Inteligência
            </strong>
            foi processado com sucesso e já está disponível para análise.

        </p>

        <p style='font-family:Arial;
                  font-size:15px;
                  color:#333;'>

            A planilha Excel segue anexada contendo os principais indicadores, análises e oportunidades identificadas no
            período avaliado.

        </p>

        <p style='font-family:Arial;
                  font-size:15px;
                  color:#333;'>

            O relatório contém:

        </p>

        <ul style='font-family:Arial;
                   font-size:15px;
                   color:#333;'>

            <li>Resumo Executivo</li>

            <li>Compras Mensais</li>

            <li>Top Fornecedores</li>

            <li>ABC Fornecedores</li>

            <li>Top Produtos</li>

            <li>Base Produtos</li>
            
            <li>ABC Produtos</li>

            <li>Top Oportunidades</li>

            <li>Oportunidades de Economia</li>

            <li>Variação de Preços</li>

            <li>Evolução Histórica</li>
            
            

        </ul>
        
        <ul>
        A aba Evolução Histórica apresenta o histórico cronológico das compras por item, permitindo analisar a
        evolução dos fornecedores, dos custos unitários, das quantidades adquiridas e dos valores totais
        comprados ao longo do período avaliado.
        
        </ul>
        

        <p style='font-family:Arial;
                  font-size:15px;
                  color:#333;'>

            Algumas oportunidades
            classificadas como
            <strong>ANOMALIA</strong>
            podem decorrer de:

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