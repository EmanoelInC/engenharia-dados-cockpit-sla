import pandas as pd
import sqlite3

def executar_pipeline_sla():
    print("=== Iniciando Pipeline de Auditoria de SLAs ===")
    
    # Simulação das tabelas brutas extraídas do TMWS / WMS Infolog
    dados_expedicao = {
        'ID_Nota_Fiscal': [1001, 1002, 1003, 1004, 1005],
        'Transportadora': ['RIOLOG', 'EFATÁ 19', 'JUCURUTU', 'RIOLOG', 'CARFELOG'],
        'Janela_Agendada': ['05:00', '05:00', '06:00', '06:00', '07:00'],
        'Horario_Saida': ['05:15', '05:45', '06:10', '06:05', '07:02'],
        'Volume_Tons': [45.2, 38.1, 12.5, 55.0, 22.8]
    }
    
    df_exp = pd.DataFrame(dados_expedicao)
    
    # Criando um banco de dados em memória para demonstrar proficiência em SQL (SQLite)
    conn = sqlite3.connect(':memory:')
    df_exp.to_sql('expedicao', conn, index=False, if_exists='replace')
    
    # Query Avançada simulando uso de Window Functions e Regras de SLA (Tolerância de 30 min)
    query_auditoria = """
    WITH CalculoTempo AS (
        SELECT *,
            CAST(SUBSTR(Horario_Saida, 1, 2) AS INT) * 60 + CAST(SUBSTR(Horario_Saida, 4, 2) AS INT) AS minutos_saida,
            CAST(SUBSTR(Janela_Agendada, 1, 2) AS INT) * 60 + CAST(SUBSTR(Janela_Agendada, 4, 2) AS INT) AS minutos_agendados
        FROM expedicao
    )
    SELECT 
        ID_Nota_Fiscal,
        Transportadora,
        Janela_Agendada,
        Horario_Saida,
        Volume_Tons,
        (minutos_saida - minutos_agendados) AS Minutos_Atraso,
        CASE 
            WHEN (minutos_saida - minutos_agendados) <= 30 THEN 1.0 
            ELSE 0.0 
        END AS Status_SLA
    FROM CalculoTempo
    """
    
    df_resultado = pd.read_sql_query(query_auditoria, conn)
    
    # Calculando KPI Ouro: iDeliver (Nível de Serviço Geral)
    ideliver_geral = df_resultado['Status_SLA'].mean() * 100
    
    print(f"\n -> Painel de Auditoria de SLAs (iDeliver Geral: {ideliver_geral:.2f}%)")
    print(df_resultado.to_string(index=False))
    
    conn.close()

if __name__ == "__main__":
    executar_pipeline_sla()