import os
import pandas as pd
import sqlite3

def gerar_excel_demonstracao_logistica():
    """
    Gera automaticamente o arquivo Excel do Cockpit com dados mascarados
    caso ele não exista localmente, preservando o sigilo corporativo.
    """
    nome_arquivo = "COCKPIT CDDNPA - MAI 2025.xlsx"
    
    if os.path.exists(nome_arquivo):
        return
        
    print(f" -> Criando arquivo Excel de demonstração com dados mascarados: {nome_arquivo}")
    
    # Aba 1: MÉTRICAS (Definições de tolerância contratuais e SLAs)
    df_metricas = pd.DataFrame({
        'Indicador': ['Avarias', 'Recepção de transferência', 'Cumprimento dos horários de janela de expedição'],
        'Tolerância_SLA': ['=< 0.1', '=> 0.95', '=> 0.95'],
        'Unidade_Medida': ['R$/ton líquido', '%', '%']
    })
    
    # Aba 2: COCKPIT (Histórico de performance mensal real acumulada)
    df_cockpit = pd.DataFrame({
        'Indicador': ['Avaria', 'Recepção de transferência via DNN Poços de Caldas', 'Cumprimento dos horários de janela de expedição', 'iDeliver Nível de Serviço'],
        'Meta_Limite': ['<= 0.1000', '>= 0.9500', '>= 0.9500', '>= 0.9000'],
        'Resultado_Maio_2025': [0.0000, 1.0000, 1.0000, 0.9973]
    })
    
    with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
        df_metricas.to_excel(writer, sheet_name='MÉTRICAS', index=False)
        df_cockpit.to_excel(writer, sheet_name='COCKPIT', index=False)

def executar_pipeline_sla():
    print("=== Iniciando Pipeline de Auditoria de SLAs (Cockpit) ===")
    
    # Garante a existência do arquivo físico .xlsx mascarado
    gerar_excel_demonstracao_logistica()
    
    # Leitura e carregamento para processamento analítico
    caminho_arquivo = "COCKPIT CDDNPA - MAI 2025.xlsx"
    df_painel = pd.read_excel(caminho_arquivo, sheet_name='COCKPIT')
    
    # Criação de Banco de Dados SQL em memória RAM para execução de queries de auditoria
    conn = sqlite3.connect(':memory:')
    df_painel.to_sql('cockpit_consolidado', conn, index=False, if_exists='replace')
    
    # Query SQL avaliando se os resultados atingiram as metas operacionais estipuladas
    query_analise = """
        SELECT 
            Indicador,
            Meta_Limite,
            Resultado_Maio_2025,
            CASE 
                WHEN Indicador = 'Avaria' AND Resultado_Maio_2025 == 0 THEN 'SLA Atingido (Excelente)'
                WHEN Resultado_Maio_2025 >= 0.95 THEN 'SLA Atingido (Conforme)'
                ELSE 'SLA Fora do Limite'
            END AS Status_SLA
        FROM cockpit_consolidado
    """
    
    df_resultado_sql = pd.read_sql_query(query_analise, conn)
    
    print("\n -> Relatório de Auditoria de Nível de Serviço extraído via SQL:")
    print(df_resultado_sql.to_string(index=False))
    
    conn.close()
    print("\n=== Pipeline de Engenharia de Dados finalizado com sucesso! ===")

if __name__ == "__main__":
    executar_pipeline_sla()
