# compras_200_relatorio_executivo.py
# ============================================================
# CRIAÇÃO DA TABELA TB_RELATORIO_EXECUTIVO
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_relatorio_executivo
    """)

    con.execute("""

        CREATE TABLE tb_relatorio_executivo AS

        SELECT

            r.valor_total_comprado,

            r.quantidade_total_comprada,

            r.produtos_distintos,

            r.fornecedores_distintos,

            r.meses_periodo,

            r.compra_media_mensal,

            r.maior_mes_compra,

            r.valor_maior_mes,

            r.menor_mes_compra,

            r.valor_menor_mes,

            s.oportunidades_totais,

            s.qtd_normal,

            s.qtd_atencao,

            s.qtd_anomalia,

            s.saving_total,

            s.saving_medio,

            s.maior_saving,

            s.maior_saving_normal,

            s.maior_saving_atencao,

            s.maior_saving_anomalia,

            i.inflacao_media_periodo

        FROM tb_resumo_executivo r

        CROSS JOIN tb_resumo_saving s

        CROSS JOIN (

            SELECT

                ROUND(
                    AVG(inflacao_media),
                    2
                ) AS inflacao_media_periodo

            FROM tb_inflacao_compras

        ) i

    """)

    relatorio = con.execute("""

        SELECT *

        FROM tb_relatorio_executivo

    """).fetchone()

    print(relatorio)

    print(
        "\n======== RELATORIO EXECUTIVO ========\n"
    )

    print(
        f"Valor Total Comprado: "
        f"{relatorio[0]:,.2f}"
    )

    print(
        f"Quantidade Comprada: "
        f"{relatorio[1]:,.2f}"
    )

    print(
        f"Produtos Distintos: "
        f"{relatorio[2]}"
    )

    print(
        f"Fornecedores Distintos: "
        f"{relatorio[3]}"
    )

    print(
        f"Meses do Periodo: "
        f"{relatorio[4]}"
    )

    print(
        f"Compra Media Mensal: "
        f"{relatorio[5]:,.2f}"
    )

    print(
        f"Maior Mes: "
        f"{relatorio[6]}"
    )

    print(
        f"Valor do Maior Mes: "
        f"{relatorio[7]:,.2f}"
    )

    print(
        f"Menor Mes: "
        f"{relatorio[8]}"
    )

    print(
        f"Valor do Menor Mes: "
        f"{relatorio[9]:,.2f}"
    )

    print()

    print(
        f"Oportunidades Totais: "
        f"{relatorio[10]}"
    )

    print(
        f"NORMAL: "
        f"{relatorio[11]}"
    )

    print(
        f"ATENCAO: "
        f"{relatorio[12]}"
    )

    print(
        f"ANOMALIA: "
        f"{relatorio[13]}"
    )

    print(
        f"Saving Total: "
        f"{relatorio[14]:,.2f}"
    )

    print(
        f"Saving Medio: "
        f"{relatorio[15]:,.2f}"
    )

    print(
        f"Maior Saving: "
        f"{relatorio[16]:,.2f}"
    )

    print(
        f"Maior Saving NORMAL: "
        f"{relatorio[17]:,.2f}"
    )

    print(
        f"Maior Saving ATENCAO: "
        f"{relatorio[18]:,.2f}"
    )

    print(
        f"Maior Saving ANOMALIA: "
        f"{relatorio[19]:,.2f}"
    )

    print()

    print(
        f"Inflacao Media de Compras: "
        f"{relatorio[20]}%"
    )

    con.close()