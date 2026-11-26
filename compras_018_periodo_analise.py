# compras_018_periodo_analise.py
# ============================================================
# CRIAÇÃO DA TABELA TB_PERIODO_ANALISE
# E RECORTE DE ATÉ 24 MESES FECHADOS EM TB_COMPRAS_VALIDADA
# ============================================================
import duckdb


def run(caminho_banco):
    con = duckdb.connect(
        caminho_banco,
        read_only=False
    )

    total_antes = con.execute("""
        SELECT COUNT(*)
        FROM tb_compras_validada
    """).fetchone()[0]

    con.execute("""
        DROP TABLE IF EXISTS
        tb_periodo_analise
    """)

    # Ancora a data final no último dia do mês anterior ao mês corrente
    # e a data inicial 23 meses antes (totalizando 24 meses fechados)
    con.execute("""
        CREATE TABLE tb_periodo_analise AS
        WITH limites AS (
            SELECT
                (DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '24 month')::DATE AS data_inicio,
                (DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 day')::DATE AS data_fim
        )
        SELECT
            data_fim,
            data_inicio,
            24 AS meses_analisados
        FROM limites
    """)

    # Filtra tb_compras_validada mantendo apenas registros dentro da janela de 24 meses
    con.execute("""
        CREATE OR REPLACE TABLE tb_compras_validada AS
        SELECT
            v.*
        FROM tb_compras_validada v
        CROSS JOIN tb_periodo_analise p
        WHERE v.data_nf::DATE >= p.data_inicio
          AND v.data_nf::DATE <= p.data_fim
    """)

    periodo = con.execute("""
        SELECT
            data_inicio,
            data_fim,
            meses_analisados
        FROM tb_periodo_analise
    """).fetchone()

    total_depois = con.execute("""
        SELECT COUNT(*)
        FROM tb_compras_validada
    """).fetchone()[0]

    descartados = total_antes - total_depois

    print("\n======== PERÍODO DE ANÁLISE ========\n")
    print(f"Data Inicial: {periodo[0]}")
    print(f"Data Final: {periodo[1]}")
    print(f"Meses Analisados: {periodo[2]}")
    print(f"Registros antes do filtro: {total_antes}")
    print(f"Registros mantidos (até 24 meses): {total_depois}")
    print(f"Registros descartados fora do período: {descartados}")

    con.close()


# ============================================================
# TESTE LOCAL
# ============================================================
if __name__ == "__main__":
    run("compras_inteligencia.duckdb")