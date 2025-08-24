# RELEASE NOTES

As versões descritas são disponíveis nas respectivas TAGs do git no repositório.

## v0.6.0 - Agora gerando arquivos json também.

O Flag --json foi adicionado para gerar arquivos `.json` com a saida neste formato para processamento
automatizado por outras rotinas e outros sistemas.

Resumo das funcionalidades implementadas na versão 0.6.0

- JSONSerializableMixin implementado conforme solicitado

Métodos from_json() e as_json()
Suporte para serialização de tipos especiais (datetime)
Usado como base para todas as classes de resultado

- Estrutura completa de classes de dados

CatalogResult: Classe base com informações comuns
SchemasResult, TablesResult, DescribeResult, QueryResult, InfoResult: Classes específicas para cada comando
TableStructure e DatabaseInfo: Classes auxiliares

- Suporte ao flag --json em todos os comandos

--json / -j: Ativa saída JSON
--output / -o: Salva em arquivo
Mantém compatibilidade com saída formatada (padrão)

- Modo interativo com toggle JSON

Comando json alterna entre modos
Estado persistente durante a sessão
Help atualizado

- Testes adicionandos

Testes para serialização

## v5.0.0 - Refatoração do código para melhor Manutenibilidade do Modulo.

A estrutura de diretórios foi modificada adicionando 7 novos arquivos Python (catalog.py, display.py,  
exceptions.py, test_main.py, test_catalog.py, test_display.py, test_exceptions.py).

```txt
psql-catalog/
├── src/
│   └── psql_catalog/
│       ├── __init__.py          # Imports e exports principais
│       ├── main.py              # CLI interface (Typer commands)
│       ├── catalog.py           # PostgreSQLCatalog class
│       ├── display.py           # Funções de formatação Rich
│       ├── exceptions.py        # Exceções customizadas
│       └── README.md
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_catalog.py          # Testes para PostgreSQLCatalog
│   ├── test_display.py          # Testes para funções display
│   └── test_exceptions.py       # Testes para exceções
├── pyproject.toml
├── .python-version
├── uv.lock
└── README.md
```

### Vantagens da Refatoração

1. Separação de Responsabilidades

- main.py: Interface CLI (Command Line Interface)
- catalog.py: Lógica de acesso ao banco de dados
- display.py: Formatação e exibição
- exceptions.py: Tratamento de erros

2. Reutilização

Agora você pode usar a classe independentemente da CLI

```python
from psql_catalog import PostgreSQLCatalog

with PostgreSQLCatalog("postgresql://...") as catalog:
    tables = catalog.list_tables('public')
    # usar em outros projetos
```

3. Testabilidade

- Cada módulo pode ser testado independentemente
- Mocks mais fáceis de implementar
- Cobertura de testes mais granular

4. Manutenibilidade

- Código mais organizadode e modular
- Fácil de encontrar e modificar funcionalidades específicas
- Menor acoplamento entre componentes

5. Extensibilidade

- Fácil adicionar novos comandos CLI
- Fácil adicionar novos métodos ao catalog
- Fácil adicionar novas formas de exibição

## v0.4.5 - Versão com funcionalidades básicas + restrições de integridade

Versão com funcionalidades básicas e display de restrições de integridade (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK)

## v0.4.0 - Versão com funcionalidades básicas

Versão com funcionalidades básicas sem considerar as restrições de integridade do Schema
