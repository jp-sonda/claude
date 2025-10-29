# O prefixo mnb_ refere-se a Marimo Notebook

import marimo

__generated_with = "0.17.2"
app = marimo.App(
    width="medium",
    app_title="Consultas por similaridade",
    auto_download=["ipynb"],
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Veja [Marimo](https://realpython.com/marimo-notebook/)""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    # PM-RAG

    ## Detecção de Anomalias (AD) em Séries Temporais Multivariadas (MTS)

    #### Keywords

    - AD - Anomaly Detection
    - MTS - Multivariate Time Series

    ## Objetivo

    - Ganhos de produtividade e vantagens competitivas em aplicações industriais
    - Identificar mau funcionamento de equipamentos ou ineficiências de processo
    - Identificar potenciais riscos de segurança
    - Implementação de manutenção preditiva e prevenção de falhas dispendiosas
    - Em busca da Manufatura com Zero Defeitos (ZDM) e Manufatura com Zero Desperdício (ZWM)

    Séries Temporais Multivariadas (MTS) são caracterizadas por complexas dependências temporais e interações entre variáveis. Ambientes industriais precisam de ferramentas robustas que implementem AD para MTS.

    AD para MTS é um desafio de pesquisa cada vez mais crítico em aplicações industriais. 
    Métodos de aprendizado supervisionado são caros.
    A alta dimensionalidade das MTS apresenta complexidades adicionais
    Problemas relacionados à qualidade dos dados na Industria (Datasets desbalanceados com pouca informação para processos anômalos) 

    Para enfrentar esses desafios, várias técnicas de processamento de sinal e ML foram propostas. Embora as técnicas de incorporação (Embedding) podem representar de dados MTS em um espaço transformado existem outros modelos importantes.

    Modelos:

    - Transformadas Wavelet fornecem novas oportunidades para detecção de anomalias mais robusta. Transformadas Wavelet Discretas (DWTs) fornecem uma ferramenta para analisar sinais não estacionários típicos em ambientes industriais. Possuem capacidade de análise multirresolução nas escalas de tempo e frequências.
    - Os autoencoders (AEs) são técnicas poderosas para criar representações vetoriais de MTS. Quando combinados com a DWT, é possível aproveitar tanto as propriedades de decomposição em escala temporal da DWT quanto as capacidades de redução de dimensionalidade dos AEs. Essa abordagem híbrida permite uma captura mais eficaz de padrões complexos e anomalias em séries temporais (TS) industriais.
    - Juntamente com os AEs, vários algoritmos de aprendizado de máquina (ML) que capturam a dependência temporal são comumente usados para detecção de anomalias (GRU, LSTM, CNN unidimensional).
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    **Diagrama de componentes**

    Veja arquivo em `docs/img/pm-rag-01.svg`
    """
    )
    return


@app.cell
def _():
    from pm_rag.util import DB_CONFIG, exec_os_command, exec_query, test_similarity_search
    return DB_CONFIG, exec_os_command, exec_query, test_similarity_search


@app.cell
def _():
    import sys
    from pathlib import Path
    import time
    import psycopg
    from pgvector.psycopg import register_vector
    from sqlalchemy import create_engine, text
    import numpy as np
    import pandas as pd

    import marimo as mo

    # Adiciona o diretório ao path para importar o módulo run_sql
    sys.path.insert(0, str(Path(__file__).parent))
    return mo, pd


@app.cell
def _(pd):
    pd.set_option('display.max_columns', None)  # para mostrar um número ilimitado de colunas
    pd.set_option('display.max_rows', None)  # para mostrar todas as linhas
    pd.set_option('display.width', 2000)  # Configura a largura da tela para um valor arbitrariamente grande
    return


@app.cell
def _():
    # DB_CONFIG é importado de util.py
    return


@app.cell
def _(DB_CONFIG, exec_os_command):
    # Verificar se PostgreSQL está rodando
    command = ["pg_isready", "-h", str(DB_CONFIG['host']), "-p", str(DB_CONFIG['port'])]
    std_out, stderr = exec_os_command(command)
    print(f"{std_out}{stderr}")
    return


@app.cell
def _(DB_CONFIG):
    print(f"Conectando ao Postgres em {DB_CONFIG['host']}")
    from pm_rag.util import (
        get_connection_string,
        get_sqlalchemy_connection_string,
        create_psycopg_connection,
        create_sqlalchemy_engine,
    )

    print(f"sqlalchemy_connection_string = {get_sqlalchemy_connection_string()}")
    return


@app.cell
def _(exec_query):
    df1 = exec_query("get_maintenance_text")
    print(df1)
    return


@app.cell
def _(exec_query):
    df2 = exec_query("get_distinct_order_type")
    print(df2)
    return


@app.cell
def _(exec_query):
    df3 = exec_query("equipment_maintainance_priority")
    print(df3)
    return


@app.cell
def _(test_similarity_search):
    test_similarity_search()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Considere a query abaixo onde a tabela `sap_pm_rag_data`  possui os dados de manutenção de uma usina de geração de energia elétrica obtidos do SAP-PM.

    ```sql
    SELECT sap_order_id, equipment_number, order_type,
           LEFT(maintenance_text, 120) as preview,
           embedding <=> %s::vector as distance  -- ⭐ OPERADOR CHAVE. %s resolve para o vetor de entrada
    FROM sap_pm_rag_data
    ORDER BY distance  -- Ordena do mais similar (menor distância)
    LIMIT 5;           -- Retorna apenas os top 5
    ```

    #### O que faz:

    Este é um comando de **busca por similaridade vetorial** (Semantic Search / RAG) que encontra as **5 ordens de manutenção mais similares** a um dado vetor de consulta.


    #### 🔍 Operador `<=>`

    O operador `<=>` é o **operador de distância de cosseno** do pgvector:

    - **Entrada**: `%s::vector` → vetor de consulta (embedding de 512 dimensões)
    - **Cálculo**: Distância de cosseno entre cada `embedding` da tabela e o vetor de consulta
    - **Saída**: Valor entre `0` e `2`
      - `0` = vetores idênticos (100% similar)
      - `1` = vetores ortogonais (sem similaridade)
      - `2` = vetores opostos

    **Quanto MENOR a distância, MAIOR a similaridade semântica.**

    ---

    #### 🎯 Objetivo no Contexto SAP-PM

    ##### Cenário de uso prático:

    **1. Usuário faz uma pergunta:**
    > "Como resolver vibração alta no mancal da turbina?"

    **2. Sistema converte a pergunta em embedding (512 dimensões)**

    ```python
    query_embedding = model.embed("Como resolver vibração alta no mancal da turbina?")
    # Resultado: [0.234, -0.123, 0.567, ..., 0.089]  # 512 valores
    ```

    **3. Query SQL busca ordens similares:**

    ```sql
    -- Substitui %s pelo query_embedding
    embedding <=> '[0.234, -0.123, 0.567, ...]'::vector
    ```

    **4. Resultado esperado (top 5):**
    ```
    | sap_order_id | equipment_number | order_type | preview                                      | distance |
    |--------------|------------------|------------|----------------------------------------------|----------|
    | 40001001     | T-01-A          | PM01       | Aumento de vibração detectado no mancal 3B... | 0.0234   |
    | 70005005     | B-01-A          | PM01       | Relatório de Análise - Bomba com vibração... | 0.0456   |
    | 40010010     | TR-FAN-04       | PM01       | Ruído excessivo no ventilador. Desbalancea...| 0.0678   |
    | 40015015     | M-01-A          | PM01       | Alto consumo de potência. Vibração com freq...| 0.0891   |
    | 40011011     | TG-02-A         | PM01       | Falha na partida da turbina a gás...        | 0.1023   |
    ```

    ---

    ## 💡 Casos de Uso na Usina

    ### 1. **Diagnóstico Assistido por IA**
    - Técnico: "Mostre as ordens de manutenção típicas para: Temperatura alta no transformador"
    - Sistema: Retorna ordens similares → `50007007` (DGA - **Dissolved Gas Analysis** em transformador) ...

    ### 2. **Busca de Soluções Históricas**
    - Pergunta: "O que tem no database sobre: Vazamento no selo da bomba"
    - Sistema: Encontra `40016016` (falha repetitiva em selo por cavitação)

    ### 3. **Análise de Causa-Raiz**
    - Query: "Qual a causa-raiz para: Queda súbita de pressão"
    - Sistema: Retorna `40003003` (vazamento na caldeira), `40013013` (selo do reator)

    ### 4. **Recomendação de Procedimentos**
    - Input: "Procedimento de partida da turbina"
    - Sistema: Retorna `60019019` (Documento PR-OP-01 completo)

    ### 5. **Correlação de Falhas**
    - **Query embedding de série temporal anormal**
    - Sistema: Encontra ordens com padrões similares de vibração/temperatura

    ---

    #### 🔧 Por que usar Embeddings?

    **Busca tradicional (SQL LIKE):**
    ```sql
    WHERE maintenance_text LIKE '%vibração%'  -- Só encontra palavra exata
    ```
    ❌ Não encontra: "oscilação", "desbalanceamento", "RMS alto"

    **Busca semântica (Embeddings):**
    ```sql
    WHERE embedding <=> query_vector  -- Entende significado
    ```
    ✅ Encontra: "vibração", "ruído", "desbalanceamento", "pico RMS"

    ---

    #### 📈 Benefícios no SAP-PM

    1. **RAG (Retrieval-Augmented Generation)**: LLM usa ordens similares como contexto
    2. **Manutenção Preditiva**: Correlaciona falhas antes de acontecerem
    3. **Knowledge Base Inteligente**: 20+ anos de histórico SAP acessível semanticamente
    4. **Redução de Downtime**: Técnico encontra solução em segundos vs. horas

    ---

    #### 🎯 Resumo

    Este comando é o **coração de um sistema RAG** para manutenção industrial, permitindo buscar conhecimento histórico do SAP-PM por **significado**, não apenas por palavras-chave exatas.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## 🔍 Query Embedding de Série Temporal Anormal - Detalhamento

    ### 📊 O Conceito

    Uma **série temporal anormal** é um padrão de dados de sensores que se desvia do comportamento normal, indicando potencial falha. Em vez de buscar por palavras-chave, você converte esse padrão anormal em um embedding e busca ordens de manutenção com padrões similares.

    ---

    ## 🎯 Como Funciona na Prática

    ### **Cenário Real:**

    Você está monitorando a **Bomba B-25-C** em tempo real:

    ```
    Tag: V-B25C (Vibração)
    Comportamento Normal: 0.5-1.2 mm/s RMS (estável)
    Comportamento Atual: 
      - Hora 0: 1.5 mm/s
      - Hora 2: 2.3 mm/s
      - Hora 4: 3.8 mm/s
      - Hora 6: 5.2 mm/s  ⚠️ ANORMAL!
    ```

    ---

    ## 🔄 Fluxo Completo do Processo

    ### **Etapa 1: Detecção da Anomalia**

    ```python
    # Sistema de monitoramento detecta padrão anormal
    def detectar_anomalia(tag: str, janela_tempo: int = 24):
        \"""
        Detecta anomalias em séries temporais usando técnicas como:
        - Z-score (desvio padrão)
        - Isolation Forest
        - LSTM Autoencoder
        \"""
        dados = buscar_dados_sensor(tag, janela_tempo)

        # Exemplo: Detecção simples por threshold
        media = np.mean(dados['valor'])
        std = np.std(dados['valor'])
        z_score = (dados['valor'][-1] - media) / std

        if z_score > 3:  # 3 desvios padrão
            return {
                'anomalia': True,
                'tag': tag,
                'tipo': classificar_anomalia(dados),
                'serie_temporal': dados
            }

        return {'anomalia': False}

    # Resultado da detecção
    anomalia = {
        'anomalia': True,
        'tag': 'V-B25C',
        'tipo': 'aumento_progressivo',  # Padrão identificado
        'serie_temporal': {
            'valores': [1.5, 2.3, 3.8, 5.2],
            'timestamps': ['2024-10-28 00:00', '02:00', '04:00', '06:00'],
            'taxa_crescimento': 0.62  # mm/s por hora
        }
    }
    ```

    ---

    ### **Etapa 2: Converter Série Temporal em Texto Descritivo**

    O embedding funciona melhor com texto rico em contexto semântico:

    ```python
    def serie_temporal_para_texto(anomalia: dict) -> str:
        \"""
        Converte a série temporal anormal em descrição textual
        \"""
        dados = anomalia['serie_temporal']

        # Gera descrição rica em contexto
        texto = f\"""
        Análise de anomalia detectada no sensor {anomalia['tag']}:

        Padrão observado: {anomalia['tipo']}

        Série temporal:
        - Valor inicial: {dados['valores'][0]} mm/s RMS
        - Valor final: {dados['valores'][-1]} mm/s RMS
        - Taxa de crescimento: {dados['taxa_crescimento']} mm/s por hora
        - Duração: {len(dados['valores'])} horas

        Características:
        - Aumento progressivo e contínuo da vibração
        - Padrão lento de deterioração
        - Sem oscilações bruscas
        - Curva de crescimento aproximadamente linear

        Contexto do equipamento:
        - Tag: V-B25C (Sensor de vibração)
        - Equipamento: Bomba de alimentação
        - Threshold de alarme: 4.0 mm/s RMS
        - Status: ALERTA - Valor acima do threshold

        Comportamento similar a falhas de:
        - Desalinhamento de eixo
        - Desgaste de rolamento
        - Desbalanceamento mecânico
        \"""

        return texto.strip()
    ```

    **Resultado:**
    ```
    "Análise de anomalia detectada no sensor V-B25C: Padrão observado: aumento_progressivo
    Série temporal: Valor inicial: 1.5 mm/s RMS, Valor final: 5.2 mm/s RMS
    Taxa de crescimento: 0.62 mm/s por hora, Duração: 4 horas
    Características: Aumento progressivo e contínuo da vibração, Padrão lento de deterioração..."
    ```

    ---

    ### **Etapa 3: Gerar Embedding da Descrição**

    ```python
    def gerar_embedding_anomalia(texto_descritivo: str) -> list[float]:
        \"""
        Gera embedding da descrição da série temporal anormal
        \"""
        # Usando OpenAI (exemplo)
        import openai

        response = openai.Embedding.create(
            input=texto_descritivo,
            model="text-embedding-ada-002"
        )

        return response['data'][0]['embedding']  # 512 ou 1536 dimensões

    # Gera o embedding
    query_embedding = gerar_embedding_anomalia(serie_temporal_para_texto(anomalia))
    # Resultado: [0.234, -0.123, 0.567, ..., 0.089]  (512 valores)
    ```

    ---

    ### **Etapa 4: Buscar Ordens Similares no PostgreSQL**

    ```sql
    -- Busca ordens de manutenção com padrões similares de vibração
    SELECT 
        sap_order_id,
        equipment_number,
        functional_location,
        order_type,
        creation_date,
        LEFT(maintenance_text, 300) AS preview,
        embedding <=> %s::vector AS distance,
        CASE 
            WHEN maintenance_text ILIKE '%vibra%' THEN 'VIBRAÇÃO'
            WHEN maintenance_text ILIKE '%rolamento%' THEN 'ROLAMENTO'
            WHEN maintenance_text ILIKE '%desalinhamento%' THEN 'DESALINHAMENTO'
        END AS tipo_falha_identificado
    FROM 
        sap_pm_rag_data
    WHERE 
        -- Filtros adicionais para refinar
        (maintenance_text ILIKE '%vibra%' 
         OR maintenance_text ILIKE '%aumento progressivo%'
         OR maintenance_text ILIKE '%mm/s%')
        AND embedding <=> %s::vector < 0.4  -- Threshold de similaridade
    ORDER BY 
        distance ASC
    LIMIT 10;
    ```

    ---

    ### **Etapa 5: Resultado da Busca**

    ```python
    # Executando a query
    resultados = executar_busca_similaridade(query_embedding)

    # Exemplo de resultado
    \"""
    | ordem_id  | equipamento | preview                                              | distance | tipo_falha      |
    |-----------|-------------|------------------------------------------------------|----------|-----------------|
    | 70005005  | B-01-A      | Relatório: vibração indica aumento progressivo...    | 0.0234   | VIBRAÇÃO        |
    |           |             | espectro de 2X RPM nas últimas 800 horas...         |          | ROLAMENTO       |
    |-----------|-------------|------------------------------------------------------|----------|-----------------|
    | 40001001  | T-01-A      | Aumento de vibração detectado no mancal 3B...        | 0.0456   | VIBRAÇÃO        |
    |           |             | pico de 12 mm/s, desalinhamento do eixo...          |          | DESALINHAMENTO  |
    |-----------|-------------|------------------------------------------------------|----------|-----------------|
    | 40010010  | TR-FAN-04   | Ruído excessivo... vibração estava 5x o limite...    | 0.0678   | VIBRAÇÃO        |
    \"""
    ```

    ---

    ## 🎯 Análise dos Resultados

    ### **Ordem 70005005 (Mais Similar - 0.0234)**

    Do dataset fornecido:

    ```
    BOMBA_ALIMENTACAO_01 | PM01 | Relatório de Análise de Vida Útil - Bomba B-01-A
    "As análises de vibração (tag: V-B01A) indicam um aumento progressivo e lento 
    do espectro de 2X RPM nas últimas 800 horas de operação. Este padrão de série 
    temporal lenta é característico de desalinhamento ou desgaste de rolamentos..."

    Detalhes da Falha de Rolamento: "O aumento da temperatura (tag: T-B01A-ROL) 
    foi o primeiro indicador, subindo de 45 para 65 em 10 dias..."
    ```

    **O que o sistema identifica:**
    - ✅ Padrão similar: "aumento progressivo e lento"
    - ✅ Tipo de falha: Rolamento desgastado
    - ✅ Solução histórica: Troca de rolamentos SKF 6210 C3
    - ✅ Correlação: Vibração + Temperatura
    - ✅ Tempo de deterioração: 800 horas (similar ao padrão atual)

    ---

    ## 💡 Sistema Completo em Produção

    ```python
    class SistemaRAGSerieTemporalAnormal:
        \"""
        Sistema completo de detecção e correlação de anomalias
        \"""

        def __init__(self):
            self.detector_anomalias = DetectorAnomalias()
            self.gerador_embeddings = GeradorEmbeddings()
            self.db = PostgreSQLConnection()

        def monitorar_e_diagnosticar(self, tag: str):
            \"""
            Pipeline completo: Monitoramento → Detecção → RAG → Diagnóstico
            \"""
            # 1. Detecta anomalia na série temporal
            anomalia = self.detector_anomalias.detectar(tag)

            if not anomalia['anomalia']:
                return {"status": "normal"}

            # 2. Converte série temporal em texto descritivo
            texto_descritivo = self.serie_temporal_para_texto(anomalia)

            # 3. Gera embedding
            query_embedding = self.gerador_embeddings.gerar(texto_descritivo)

            # 4. Busca ordens similares
            ordens_similares = self.buscar_ordens_similares(query_embedding)

            # 5. Envia para LLM para diagnóstico
            diagnostico = self.gerar_diagnostico_llm(
                anomalia=anomalia,
                ordens_similares=ordens_similares
            )

            return {
                "status": "anomalia_detectada",
                "tag": tag,
                "anomalia": anomalia,
                "ordens_similares": ordens_similares,
                "diagnostico": diagnostico,
                "acoes_recomendadas": diagnostico['acoes']
            }

        def gerar_diagnostico_llm(self, anomalia, ordens_similares):
            \"""
            Usa LLM (GPT-4, Claude, etc) para gerar diagnóstico
            \"""
            contexto = "\n\n".join([
                f"Ordem {o['sap_order_id']} - {o['equipment_number']}:\n{o['maintenance_text']}"
                for o in ordens_similares
            ])

            prompt = f\"""
            Você é um especialista em manutenção de usinas de energia.

            SITUAÇÃO ATUAL:
            {self.serie_temporal_para_texto(anomalia)}

            HISTÓRICO DE CASOS SIMILARES:
            {contexto}

            Com base no histórico, forneça:
            1. Diagnóstico provável da causa raiz
            2. Tempo estimado até falha crítica
            3. Ações corretivas recomendadas (prioridade)
            4. Peças de reposição necessárias
            5. Janela de manutenção sugerida

            Formato da resposta: JSON
            \"""

            resposta = self.llm.generate(prompt)
            return json.loads(resposta)

    # Uso em produção
    sistema = SistemaRAGSerieTemporalAnormal()
    resultado = sistema.monitorar_e_diagnosticar('V-B25C')

    print(resultado['diagnostico'])
    \"""
    {
        "causa_raiz": "Desgaste de rolamento SKF 6210 C3",
        "tempo_ate_falha": "48-72 horas",
        "prioridade": "ALTA",
        "acoes_recomendadas": [
            "1. Parada programada em 24h",
            "2. Substituir rolamentos",
            "3. Verificar alinhamento do eixo",
            "4. Inspecionar base por recalque"
        ],
        "pecas_necessarias": ["SKF 6210 C3 (2 unidades)", "Acoplamento H-201"],
        "custo_estimado": "R$ 15.000",
        "downtime_estimado": "8 horas"
    }
    \"""
    ```

    ---

    ## 📊 Tipos de Padrões Detectáveis

    ### **1. Aumento Progressivo (Drift)**
    ```
    Padrão: ↗️ ↗️ ↗️ (lento e contínuo)
    Exemplo: Vibração aumentando 0.5 mm/s por dia
    Causa típica: Desgaste de rolamento, desalinhamento
    Match no dataset: Ordem 70005005 (Bomba B-01-A)
    ```

    ### **2. Oscilação Violenta**
    ```
    Padrão: ↑↓↑↓↑↓ (alta frequência)
    Exemplo: Pressão variando ±10% a cada 2 segundos
    Causa típica: Cavitação, ressonância
    Match no dataset: Ordem 40016016 (Bomba B-22-A - cavitação)
    ```

    ### **3. Queda Brusca (Step Change)**
    ```
    Padrão: ━━━━╲______ (súbito)
    Exemplo: Pressão cai 30% em 5 segundos
    Causa típica: Vazamento, ruptura
    Match no dataset: Ordem 40003003 (Caldeira - vazamento)
    ```

    ### **4. Flatline (Falha de Instrumento)**
    ```
    Padrão: ━━━━━━━━ (constante anormal)
    Exemplo: Temperatura presa em 4.00 mA
    Causa típica: Falha de sensor
    Match no dataset: Ordem 40017017 (Transmissor T-HT-05)
    ```

    ### **5. Ruído Aleatório (Noise)**
    ```
    Padrão: ∿∿∿∿∿∿ (errático)
    Exemplo: Leitura com ruído branco
    Causa típica: Interferência eletrônica, falha de cabo
    Match no dataset: Ordem SISTEMA_VIBRACAO (V-MTR-05)
    ```

    ---

    ## 🚀 Vantagens do Approach

    ### **1. Detecção Precoce**
    - Identifica falhas antes da quebra
    - Tempo: 48-72h de antecedência (vs 0h na quebra)

    ### **2. Diagnóstico Preciso**
    - Correlaciona padrão atual com histórico de 20+ anos
    - Acurácia: ~85-90% (vs 60% diagnóstico manual)

    ### **3. Manutenção Preditiva**
    - Converte PM01 (corretiva) em PM03 (preventiva)
    - Redução de custos: 40-60%

    ### **4. Transferência de Conhecimento**
    - Captura expertise de técnicos experientes
    - Democratiza conhecimento para equipe júnior

    ---

    ## 🎯 Resultado Final para o Operador

    ```
    ┌─────────────────────────────────────────────────────────────┐
    │  🚨 ALERTA PREDITIVO - BOMBA B-25-C                        │
    ├─────────────────────────────────────────────────────────────┤
    │  Tag: V-B25C                                                │
    │  Vibração: 5.2 mm/s RMS (↑ de 1.5 em 6h)                  │
    │                                                             │
    │  📊 DIAGNÓSTICO (85% confiança):                           │
    │     Desgaste de rolamento - padrão idêntico à OM 70005005  │
    │                                                             │
    │  ⏱️  TEMPO ATÉ FALHA: 48-72 horas                          │
    │                                                             │
    │  ✅ AÇÕES RECOMENDADAS:                                    │
    │     1. Programar parada em 24h                             │
    │     2. Peças: SKF 6210 C3 (2x) - Estoque: ✓               │
    │     3. Técnico: João Silva (8h expertise)                  │
    │     4. Downtime estimado: 8 horas                          │
    │                                                             │
    │  💰 ECONOMIA: R$ 45.000 (vs quebra não planejada)         │
    └─────────────────────────────────────────────────────────────┘
    ```

    ### **Isso é RAG com séries temporais anormais!** 🎯
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""Veja [Referências Aqui](http://localhost:2718/?file=tests%2Fmnb_surveys.py)""")
    return


if __name__ == "__main__":
    app.run()
