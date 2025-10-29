import marimo

__generated_with = "0.17.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Casos de Uso para Database Vetorial

    ### 1. Text to SQL

    **Aplicação psql_catalog**

    - Criar um MCP Server para reusar o psql_catalog. Pode ser extendido para outros Bancos de Dados Relacionais (MySQL, Oracle, etc.)
    - Testado com consultas em linguagem natural ao database do KeyCloak (relativamente complexo) usando o Claude ()
    - Possibilidade de 
    [Aplicação psql_catalog + Text-to-SQL (ou NL2SQL) utilizando Geração Aumentada por Recuperação (RAG) e embeddings.](http://localhost:2718/?file=tests%2Fmnb_db_schema.py)

    ### 2. Gestão de conhecimento para o NIE


    > Dado um video de tamanho arbitrário (testei com 2 horas e meia)

    Funções: 

    - ✅ Instalar dependências automaticamente (se necessário)
    - ✅ Transcrever o áudio completo
    - ✅ Detectar idioma (PT-BR, EN, etc)
    - ✅ Mostrar progresso em tempo real
    - ✅ Salvar resultado em .txt (e opcionalmente .srt para legendas)
    - ✅ Suportar diferentes modelos Whisper (base, small, medium, large)

    #### **Ainda falta:**

    - Criar código Python para gerar o schema PostgreSQL com pgvector.
    - Criar código Python para permitir a adição de conteúdo Multimodal (Embeddings de texto e correspondentes endereços nos vídeos)
    - Criar código Python para visualizar, no browser WEB, os segmentos de vídeo relacionado ao prompt do usuário.

      Exemplo: "Quem apresentou a linguagem Julia para os desenvolvedores do Cepel o que ele disse sobre geolocalização ?"

    #### **Desafios:**

    - Curadoria de Dados
    - Manutenção do Conteudo
    - Gestão MLOPS

    [Aplicação audio](http://localhost:2718/?file=tests%2Fmnb_audio.py)


    ### 3. Detecção de Anomalias em séries temporais multivariadas usando embeddings

    [file:///Users/joao/dev/claude/python/pm-rag/docs/img/pm-rag-01.jpg](file:///Users/joao/dev/claude/python/pm-rag/docs/img/pm-rag-01.jpg)

    [Aplicação pm_rag](http://localhost:2718/?file=tests%2Fmnb_queries.py) 

    > Dado que eu tenho dados de acesso a um sistema SAP-PM de uma planta industrial (usina de geração de energia, por exemplo) eu posso usar um sistema para reproduzir dados de manutenção construindo um **Data Lakehowse** (Data Lake + Data Warehowse), resumindo: dados semi-estruturados com ACID (Atomicidade, Consistência, Isolamento e Durabilidade).

    Funções: 

    - Adaptador para SAP-PM
    - Adaptador para o SOMA
    - Modelo Canônico para conhecimento estruturado com embeddings refletindo modelo do SAP-PM e softwares análogos, além do relacionamento com as séries temporais multivariadas.
    - T8sPreProcessessing
    - Vetorizer
    - QueryManager
    - ChatApp

    #### **Desafios:**

    - Curadoria de Dados
    - Manutenção do Conteudo
    - Gestão MLOPS

    #### Referências

    [Surveys e Artigos recentes sobre Industria 5.0](http://localhost:2718/?file=tests%2Fmnb_surveys.py)
    """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
