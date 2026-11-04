# compras_180_resumo_saving.py

# ============================================================
# CRIAÇÃO DA TABELA TB_RESUMO_SAVING
# ============================================================

import duckdb


def run(caminho_banco):

    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    con.execute("""
        DROP TABLE IF EXISTS
        tb_resumo_saving
    """)

    con.execute("""

        CREATE TABLE tb_resumo_saving AS

        WITH resumo AS (

            SELECT

                COUNT(*)
                    AS oportunidades_totais,

                COUNT(
                    CASE
                        WHEN status = 'NORMAL'
                        THEN 1
                    END
                ) AS qtd_normal,

                COUNT(
                    CASE
                        WHEN status = 'ATENCAO'
                        THEN 1
                    END
                ) AS qtd_atencao,

                COUNT(
                    CASE
                        WHEN status = 'ANOMALIA'
                        THEN 1
                    END
                ) AS qtd_anomalia,

                SUM(saving_absoluto)
                    AS saving_total,

                AVG(saving_absoluto)
                    AS saving_medio

            FROM tb_saving_potencial

        ),

        maior_saving AS (

            SELECT

                saving_absoluto

            FROM tb_saving_potencial

            ORDER BY saving_absoluto DESC

            LIMIT 1

        ),

        maior_normal AS (

            SELECT

                saving_absoluto

            FROM tb_saving_potencial

            WHERE status = 'NORMAL'

            ORDER BY saving_absoluto DESC

            LIMIT 1

        ),

        maior_atencao AS (

            SELECT

                saving_absoluto

            FROM tb_saving_potencial

            WHERE status = 'ATENCAO'

            ORDER BY saving_absoluto DESC

            LIMIT 1

        ),

        maior_anomalia AS (

            SELECT

                saving_absoluto

            FROM tb_saving_potencial

            WHERE status = 'ANOMALIA'

            ORDER BY saving_absoluto DESC

            LIMIT 1

        )

        SELECT

            r.oportunidades_totais,

            r.qtd_normal,

            r.qtd_atencao,

            r.qtd_anomalia,

            ROUND(
                r.saving_total,
                2
            ) AS saving_total,

            ROUND(
                r.saving_medio,
                2
            ) AS saving_medio,

            m.saving_absoluto
                AS maior_saving,

            n.saving_absoluto
                AS maior_saving_normal,

            a.saving_absoluto
                AS maior_saving_atencao,

            x.saving_absoluto
                AS maior_saving_anomalia

        FROM resumo r

        CROSS JOIN maior_saving m

        CROSS JOIN maior_normal n

        CROSS JOIN maior_atencao a

        CROSS JOIN maior_anomalia x

    """)

    resumo = con.execute("""

        SELECT *

        FROM tb_resumo_saving

    """).fetchone()

    print(
        "\n======== RESUMO DE SAVING ========\n"
    )

    print(
        f"Oportunidades Totais: "
        f"{resumo[0]}"
    )

    print(
        f"NORMAL: "
        f"{resumo[1]}"
    )

    print(
        f"ATENCAO: "
        f"{resumo[2]}"
    )

    print(
        f"ANOMALIA: "
        f"{resumo[3]}"
    )

    print(
        f"Saving Total: "
        f"{resumo[4]:,.2f}"
    )

    print(
        f"Saving Médio: "
        f"{resumo[5]:,.2f}"
    )

    print(
        f"Maior Saving: "
        f"{resumo[6]:,.2f}"
    )

    print(
        f"Maior Saving NORMAL: "
        f"{resumo[7]:,.2f}"
    )

    print(
        f"Maior Saving ATENCAO: "
        f"{resumo[8]:,.2f}"
    )

    print(
        f"Maior Saving ANOMALIA: "
        f"{resumo[9]:,.2f}"
    )

    con.close()