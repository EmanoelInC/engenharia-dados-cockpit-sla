# Pipeline de Dados e Monitoramento de SLAs Contratuais (Cockpit)

Repositório voltado à Engenharia de Dados Logísticos e Comerciais, simulando processos de governança de grandes contas (*Open Book*).

## 🚀 O que este repositório resolve?
Em grandes operações, atrasos de carregamento geram multas contratuais (penalidades LTPO). Este pipeline automatiza a auditoria de pátio extraindo dados do WMS, tratando-os via Python e rodando análises em **SQL** para travar e consolidar o indicador de **iDeliver** (Nível de Serviço).

## 📊 Diferenciais Técnicos Demonstrados:
* **SQL Avançado**: Uso de tabelas temporárias (CTEs) e condicionais complexas para apuração de metas contratuais.
* **Visão de Negócio**: Foco em zerar penalidades operacionais e gerir gargalos com transportadoras de grande escala.

## 🔒 Governança de Dados e Mascaramento
Por motivos de conformidade, confidencialidade e segurança da informação, as bases de dados reais utilizadas originalmente no ambiente corporativo foram omitidas deste repositório público. 

O script `pipeline_sla.py` possui uma camada interna que gera dados simulados perfeitamente aderentes às regras de negócio originais. Isso garante a reprodutibilidade do código e demonstra a lógica aplicada sem expor dados sensíveis.
