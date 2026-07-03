import pandas as pd
import os

def gerar_excel_demonstracao_logistica():
    nome_arquivo = "COCKPIT CDDNPA - MAI 2025.xlsx"
    
    if os.path.exists(nome_arquivo):
        return
        
    print(f" -> Criando arquivo de demonstração: {nome_arquivo}")
    
    # Dados da aba MÉTRICAS
    df_metricas = pd.DataFrame({
        'Indicador': ['Avarias', 'Recepção de transferência', 'Cumprimento de janela'],
        'Tolerância_SLA': ['=< 0.1', '=> 0.95', '=> 0.95'],
        'Unidade': ['R$/ton', '%', '%']
    })
    
    # Dados da aba COCKPIT
    df_cockpit = pd.DataFrame({
        'Mês': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio'],
        'Avaria_Resultado': [0, 0, 0, 0, 0],
        'Recepção_Aderencia': [0.99, 0.99, 1.0, 1.0, 1.0],
        'Expedicao_Janela': [1.0, 1.0, 0.99, 1.0, 1.0]
    })
    
    with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
        df_metricas.to_excel(writer, sheet_name='MÉTRICAS', index=False)
        df_cockpit.to_excel(writer, sheet_name='COCKPIT', index=False)

def executar_pipeline_sla():
    print("=== Iniciando Pipeline de Auditoria de SLAs ===")
    
    # Garante a criação do Excel
    gerar_excel_demonstracao_logistica()
    
    # Lê os dados do arquivo gerado
    df_painel = pd.read_excel("COCKPIT CDDNPA - MAI 2025.xlsx", sheet_name='COCKPIT')
    print("\n -> Histórico do Cockpit lido com sucesso:")
    print(df_painel)

if __name__ == "__main__":
    executar_pipeline_sla()
