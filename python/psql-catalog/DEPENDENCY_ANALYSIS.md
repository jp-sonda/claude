# Table Dependency Analysis

Esta extensão do psql-catalog adiciona funcionalidades para análise de dependências entre tabelas baseadas em foreign keys e geração de comandos SQL em lote na ordem correta.

## Funcionalidades Principais

### 1. Análise de Dependências (`TableDependencyGraph`)

A classe `TableDependencyGraph` analisa as foreign keys entre tabelas e constrói um grafo direcionado das dependências, permitindo:

- **Detecção de ciclos**: Identifica dependências circulares que podem causar problemas
- **Ordenação topológica**: Gera listas ordenadas de tabelas respeitando dependências
- **Análise detalhada**: Fornece informações sobre dependências diretas e indiretas

### 2. Operações em Lote (`DatabaseBatchOperations`)

A classe `DatabaseBatchOperations` gera comandos SQL em lote na ordem correta para:

- **DROP TABLE**: Para remoção segura de tabelas
- **TRUNCATE**: Para limpeza de dados respeitando foreign keys
- **INSERT**: Templates para inserção de dados na ordem correta
- **Controle de constraints**: Desabilitar/habilitar foreign keys temporariamente

## Instalação

As novas classes estão incluídas no psql-catalog. Certifique-se de que você tem a versão 0.7.0 ou superior.

```bash
pip install -e .
```

## Uso Básico

### 1. Gerar arquivo de schema

Primeiro, use o psql-catalog para gerar o arquivo JSON do schema:

```bash
psql-catalog describe-all --schema public --constraints --json --output my_schema.json --db $DB_CONN
```

### 2. Analisar dependências

```python
from psql_catalog.dependency_graph import TableDependencyGraph

# Carregar e analisar
graph = TableDependencyGraph()
graph.load_from_json_file('my_schema.json')

# Obter ordens de operação
insert_order = graph.get_insert_order()  # Para INSERT seguro
drop_order = graph.get_drop_order()      # Para DROP seguro

print(f"Ordem para INSERT: {' -> '.join(insert_order)}")
print(f"Ordem para DROP:   {' -> '.join(drop_order)}")
```

### 3. Gerar comandos em lote

```python
from psql_catalog.batch_operations import DatabaseBatchOperations

# Criar handler
batch_ops = DatabaseBatchOperations('my_schema.json')

# Gerar comandos DROP
drop_statements = batch_ops.generate_drop_statements(cascade=True)
for stmt in drop_statements:
    print(stmt)

# Salvar em arquivo SQL
batch_ops.save_sql_script('drop', 'drop_tables.sql', cascade=True)
```

## Exemplos Práticos

### Preparar Ambiente de Teste

```python
from psql_catalog.dependency_graph import analyze_schema_file
from psql_catalog.batch_operations import DatabaseBatchOperations

# Analisar schema
graph = analyze_schema_file('my_schema.json')
batch_ops = DatabaseBatchOperations('my_schema.json')

# 1. Desabilitar foreign keys
disable_fk = batch_ops.generate_disable_constraints_statements()

# 2. Truncate em ordem segura
truncate_order = graph.get_drop_order()
for table in truncate_order:
    print(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")

# 3. Reabilitar foreign keys
enable_fk = batch_ops.generate_enable_constraints_statements()

# 4. Inserir dados em ordem segura
insert_order = graph.get_insert_order()
for table in insert_order:
    print(f"-- Inserir dados em {table}")
```

### Migração de Schema

```python
# Ordem para DROP (dependentes primeiro)
drop_order = graph.get_drop_order()
print("DROP order:", " -> ".join(drop_order))

# Ordem para CREATE (dependências primeiro)
create_order = graph.get_insert_order()
print("CREATE order:", " -> ".join(create_order))
```

## Interface de Linha de Comando

### Análise de Dependências

```bash
# Análise completa
python -m psql_catalog.dependency_graph my_schema.json

# Usando o script de operações em lote
python -m psql_catalog.batch_operations analyze my_schema.json
```

### Gerar Comandos SQL

```bash
# Gerar DROP statements
python -m psql_catalog.batch_operations drop my_schema.json --output drop.sql --cascade

# Gerar TRUNCATE statements
python -m psql_catalog.batch_operations truncate my_schema.json --output truncate.sql --restart-identity

# Gerar INSERT templates
python -m psql_catalog.batch_operations insert-template my_schema.json --output insert.sql

# Apenas mostrar as ordens
python -m psql_catalog.batch_operations order my_schema.json
```

## Funções de Conveniência

```python
from psql_catalog.dependency_graph import (
    get_table_insert_order,
    get_table_drop_order,
    print_dependency_analysis
)

# Obter ordens rapidamente
insert_order = get_table_insert_order('my_schema.json')
drop_order = get_table_drop_order('my_schema.json')

# Análise completa
print_dependency_analysis('my_schema.json')
```

## Casos de Uso Comuns

### 1. **Limpeza de Ambiente de Teste**

- Truncate todas as tabelas respeitando foreign keys
- Recarregar dados de teste na ordem correta

### 2. **Backup e Restore**

- Determinar ordem correta para dump de dados
- Garantir restore sem violação de constraints

### 3. **Migração de Schema**

- DROP seguro de todas as tabelas
- CREATE na ordem correta das dependências

### 4. **Desenvolvimento e CI/CD**

- Scripts automáticos para reset de banco
- Validação de integridade referencial

## Tratamento de Casos Especiais

### Auto-Referências

Tabelas com auto-referência (como `categories.parent_id -> categories.id`) são tratadas corretamente:

```python
# A tabela categories será incluída na ordenação
# mas você pode precisar tratar os dados especialmente
insert_order = graph.get_insert_order()
# ['users', 'categories', 'products', 'orders', 'order_items']
```

### Dependências Circulares

O sistema detecta dependências circulares e lança `CycleDetectionError`:

```python
try:
    insert_order = graph.get_insert_order()
except CycleDetectionError as e:
    print(f"Dependência circular detectada: {e}")
    # Você precisará quebrar o ciclo temporariamente
```

## Estrutura dos Arquivos

```
psql_catalog/
├── dependency_graph.py      # Classe principal para análise
├── batch_operations.py      # Geração de comandos SQL
├── test_dependency_graph.py # Testes automatizados
└── usage_example.py         # Script de demonstração
```

## Executar Demonstração

Para ver todas as funcionalidades em ação:

```bash
cd /Users/joao/dev/claude/python/psql-catalog/src/psql_catalog
python usage_example.py
```

Este script criará um schema de exemplo e demonstrará todas as funcionalidades disponíveis.

## Testes

Execute os testes para validar a funcionalidade:

```bash
python test_dependency_graph.py
```

## Limitações

1. **Auto-referências**: Requerem tratamento especial dos dados
2. **Dependências circulares**: Devem ser quebradas temporariamente
3. **Triggers e procedures**: Não são analisados (apenas foreign keys)
4. **Schemas múltiplos**: Cada schema deve ser analisado separadamente

## Contribuições

Para adicionar novas funcionalidades:

1. Estenda a classe `TableDependencyGraph` para nova análise
2. Adicione métodos em `DatabaseBatchOperations` para novos tipos de comando
3. Inclua testes em `test_dependency_graph.py`
4. Documente no README e adicione exemplos

## Versionamento

- v0.7.0: Versão inicial com análise de dependências e operações em lote
- As funcionalidades são retrocompatíveis com versões anteriores do psql-catalog
