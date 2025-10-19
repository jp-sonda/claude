# Script de Criação e População da Tabela SAP PM RAG Data

## Descrição

Este projeto contém scripts Python para criar e popular uma tabela PostgreSQL com dados simulados de manutenção industrial para uso em sistemas RAG (Retrieval-Augmented Generation) com embeddings vetoriais.

## Estrutura de Arquivos

```
/Users/joao/dev/claude/python/pm-rag/tests/
├── ddl_01.py       # Definições SQL (tabela, função, dados)
├── run_sql.py      # Script principal de execução
└── README.md       # Esta documentação
```

## Pré-requisitos

### 1. PostgreSQL com extensão pgvector

```bash
# Instalar PostgreSQL (se necessário)
brew install postgresql@16

# Criar banco de dados
createdb pm_rag
```

### 2. Instalar extensão pgvector

```bash
# No PostgreSQL
CREATE EXTENSION vector;
```

### 3. Pacotes Python 3.12

```bash
# pip install numpy pgvector "psycopg[binary]" SQLAlchemy
# As dependências estão relacionadas no arquivo pyproject.toml então basta instalar:
python3 -m pip install -e .
```

## Configuração

Edite as credenciais do banco de dados em `run_sql.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5434,
    'dbname': 'pm_rag',
    'user': 'postgres',
    'password': 'postgres'
}
```

## Estrutura da Tabela

```sql
CREATE TABLE sap_pm_rag_data (
    id                  SERIAL PRIMARY KEY,
    sap_order_id        VARCHAR(12),
    functional_location VARCHAR(30),
    equipment_number    VARCHAR(18),
    order_type          VARCHAR(4),
    maintenance_text    TEXT,
    chunk_id            INTEGER,
    embedding           VECTOR(512),
    creation_date       DATE
);
```

## Execução

### Executar o script completo:

```bash
cd /Users/joao/dev/claude/python/pm-rag/tests/
python run_sql.py
```

### O script executa automaticamente:

1. ✅ Habilita a extensão pgvector
2. ✅ Cria a tabela `sap_pm_rag_data`
3. ✅ Cria a função `generate_random_embedding()`
4. ✅ Itera sobre `insert_simulated_data` executando cada INSERT
5. ✅ Faz commit das transações
6. ✅ Verifica os dados inseridos
7. ✅ Testa busca de similaridade vetorial

## Dados Simulados

O arquivo `ddl_01.py` contém **50+ comandos INSERT** simulando ordens de manutenção industrial com:

- **Tipos de ordem**: PM01 (Corretiva), PM02 (Emergencial), PM03 (Preventiva)
- **Chunks de diferentes tamanhos**: curtos (<500 chars), médios (500-1150), longos (>1150)
- **Tags de sensores**: temperatura, vibração, pressão, potência
- **Cenários realistas**: falhas, calibrações, inspeções, análises de causa-raiz

## Funcionalidades

### 1. Criação de Tabela e Função

```python
create_table_and_function()
```

Utiliza **psycopg** para executar DDL.

### 2. Inserção de Dados

```python
execute_inserts()
```

Utiliza **SQLAlchemy** para iterar sobre `insert_simulated_data` e executar cada INSERT com commit individual.

### 3. Verificação de Dados

```python
verify_data()
```

Exibe estatísticas:

- Total de registros
- Distribuição por tipo de ordem
- Distribuição por chunk
- Top 10 equipamentos
- Dimensão dos embeddings

### 4. Teste de Similaridade

```python
test_similarity_search()
```

Utiliza **numpy** para gerar um vetor aleatório e **pgvector** para buscar os 5 registros mais similares usando distância de cosseno.

## Exemplo de Saída

```
================================================================================
ETAPA 1: CRIANDO TABELA E FUNÇÃO
================================================================================

[1/4] Habilitando extensão pgvector...
✓ Extensão pgvector habilitada

[2/4] Removendo tabela existente (se houver)...
✓ Tabela anterior removida (se existia)

[3/4] Criando tabela sap_pm_rag_data...
✓ Tabela criada com sucesso

[4/4] Criando função generate_random_embedding...
✓ Função criada com sucesso

================================================================================
✓ TABELA E FUNÇÃO CRIADAS COM SUCESSO!
================================================================================

================================================================================
ETAPA 2: EXECUTANDO INSERTS
================================================================================

📊 Total de comandos na lista: 51
🔄 Iniciando inserção...

  ✓ [5 inserts executados...]
  ✓ [10 inserts executados...]
  ...
```

## Tecnologias Utilizadas

- **Python 3.12**
- **PostgreSQL** com extensão **pgvector**
- **numpy**: geração de vetores aleatórios
- **psycopg[binary]**: driver PostgreSQL
- **SQLAlchemy**: ORM e execução de SQL
- **pgvector**: suporte a embeddings vetoriais

## Casos de Uso

Este dataset é ideal para:

1. **RAG Systems**: Recuperar documentos de manutenção relevantes
2. **Machine Learning**: Treinar modelos de predição de falhas
3. **Análise de Séries Temporais**: Correlacionar vibração, temperatura e pressão
4. **Busca Semântica**: Encontrar ordens similares por embedding
5. **Sistemas de Recomendação**: Sugerir ações baseadas em histórico

## Próximos Passos

1. Substituir `generate_random_embedding()` por embeddings reais (OpenAI, Ollama, etc.)
2. Implementar pipeline de ETL para dados SAP reais
3. Criar API para busca semântica
4. Adicionar índices HNSW para busca vetorial eficiente

## Autor

Desenvolvido para o projeto PM-RAG (Predictive Maintenance - Retrieval Augmented Generation) por João Antonio Ferreira CEPEL/Eletrobras.

## Troubleshooting

### Erro: "No module named 'psycopg2'"

**Problema**: SQLAlchemy está tentando usar psycopg2 em vez de psycopg3.

**Solução**: O script já está configurado para usar `postgresql+psycopg://` na connection string do SQLAlchemy, forçando o uso do psycopg3.

### Erro: "could not connect to server"

**Problema**: PostgreSQL não está rodando ou configurações de conexão incorretas.

**Solução**:

```bash
# Verificar se PostgreSQL está rodando
pg_isready -h localhost -p 5434

# Iniciar PostgreSQL (macOS com Homebrew)
brew services start postgresql@18

# Verificar configurações em run_sql.py
DB_CONFIG = {
    'host': 'localhost',
    'port': 5434,
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres'
}
```

### Erro: "extension 'vector' does not exist"

**Problema**: Extensão pgvector não está instalada.

**Solução**:

```bash
# Instalar pgvector
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
make install  # Pode precisar de sudo

# No PostgreSQL
CREATE EXTENSION vector;
```

### Erro de permissão no banco de dados

**Problema**: Usuário não tem permissões suficientes.

**Solução**:

```sql
-- Como superusuário do PostgreSQL
GRANT ALL PRIVILEGES ON DATABASE pm_rag TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
```

## Licença

MIT
