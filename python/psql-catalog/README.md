# psql-catalog

Consulte informações sobre o catalogo PostgreSQL dado um schema e as credenciais de acesso.

## Funcionalidades

- **Navegação de Esquemas**: Liste todos os esquemas do seu banco de dados PostgreSQL
- **Listagem de Tabelas**: Visualize o nome de todas as tabelas dentro de um esquema específicado
- **Estrutura da Tabela**: Visualize Informações detalhadas das colunas, incluindo tipos de dados, nulidade e padrões
- **Informações de Índice**: Visualize todos os índices das tabelas, incluindo índices de chave primária e única
- **Restrições de Integridade**: Exiba todas as restrições de integridade, incluindo:
- Restrições de Chave Primária
- Restrições de Chave Estrangeira com ações referenciais (ON UPDATE/ON DELETE)
- Restrições de Exclusividade
- Verifique as restrições com suas condições
- **Modo Interativo**: Interface de linha de comando para facilitar a exploração do banco de dados
- **Saída Avançada**: Tabelas formatadas e bonitas usando a biblioteca avançada
- **Desempenho Rápido**: Construído com o gerenciador de pacotes UV para Desempenho superior de `build` e `deploy`
- **Multiplos Formatos de Saída**: _i)_ Rich formatted tables (default); _ii)_ JSON output with --json flag ; _iii)_ Save output to files with --output flag

## Clone e faça o build

```bash
mkdir -p $HOME/dev/claude ; cd $HOME/dev/claude
git clone ...
cd python/psql-catalog
```

Instale o gerenciador de pacotes `uv` um substituto pro pip e outros utilitários do Python.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Tipicamente o uv será instalado em $HOME/.local/bin
# O Instalador colocará uma linha no final de seu startup dda BASH ou ZSH.
# Para não precisar reicniar a BASH, execute essa linha:
. "HOME/.local/bin/env"
```

```bash
# Desativa o Virtual Environment atual. O comando uv sync criará automaticamente um ambiente Virtual.
# O gerenciador de pacotes uv não precisa de activate/deactivate. Ele gerencia automaticamente nos
# comandos uv add, av sync, etc.
deactivate
uv sync
# Pode ser necessário usar 'uv --native-tls sync' se o uv não reconhecer a cadeia de certificados CA
uv pip install -e .
# Pode ser necessário usar 'uv --native-tls pip install -e .' se o uv não reconhecer a cadeia de certificados CA
#
# Quando o projeto é compilado e construido o script python 'psql-catalog' é criado no diretório
# .venv/bin/ assim é util criar um alias para facilitar as chamadas ao CLI Python para visualização
# dos objetos do catálogo do seu Schema no PostgreSQL.
alias psql-catalog='.venv/bin/psql-catalog'
```

Com o `uv` podemos rodar a nossa CLI diretamente sem ativar manualmente o virtual environment:

```bash
uv run psql-catalog --help
# ou
psql-catalog --help
```

## Exemplo de uso

Depois de configurar o modulo, você poderá usar o seu projeto assim:

Crie uma variavel no ambiente com a String de conexão ao seu Banco de Dados, como no exemplo:

```bash
# Construa a variável DB_CONN com a URL de acesso ao database.
export DP_PORT=5432
export MY_DB="my_db_name"
export DB_CONN="postgresql://my_user:my_password@my_db_host:$DP_PORT/$MY_DB"
```

```bash
# Listar schemas
uv run psql-catalog schemas --db $DB_CONN
# ou, usando o alias:
psql-catalog schemas --db $DB_CONN

![psql-catalog-01](docs/psql-catalog-01.png docs/)

# Listar tabelas
uv run psql-catalog tables --schema public --db $DB_CONN
# ou, usando o alias:
psql-catalog tables --schema public --db $DB_CONN

# Descrever uma tabela
uv run psql-catalog describe user_entity --schema public --db $DB_CONN
# ou, usando o alias:
psql-catalog describe user_entity --schema public --db $DB_CONN
# Descrever uma tabela incluindo as retrições de integridadde (integrity constraints - PRIMARY KEY,
# FOREIGN KEY, UNIQUE, CHECK)
uv run psql-catalog describe user_entity --schema public --constraints --db $DB_CONN
# ou, usando o alias:
psql-catalog describe user_entity --schema public --constraints --db $DB_CONN

# Descrever todas as tabelas de um dado Schema incluindo as informações de retrições de
# integridadde (integrity constraints - PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK) além de
# gerar um arquivo JSON de saida para ser usada em outro processo de automação tal comoum MCP
# Server para geração de codigo SQL via consultas em linguagem natural.
uv run psql-catalog describe-all --json --schema public --constraints --output my_schema.json --db $DB_CONN
psql-catalog describe-all --json --schema public --constraints --output my_schema.json --db $DB_CONN
```

### Usando no modo interativo:

```
# Modo interativo
uv run psql-catalog interactive
```

## Por que usar o **uv** como gerenciador de pacotes Python ?

Com essa configuração você terá:

- Velocidade: O gerenciador de pacotes Python `uv` é muito mais rápido que pip/pip-tools
- Compatibilidade: Mantém a estrutura src/ que já conhecemos de outros projetos
- Gestão de dependências: Resolve dependências de forma mais eficiente
- Python 3.12+: Suporte nativo para a versão mais recente
- Desenvolvimento: Ferramentas de lint, formatação e testes já configuradas no pyproject.toml

O projeto está pronto para você começar a desenvolver seu navegador de catálogo PostgreSQL!

## Construção do Zero

As instruções abaixo foram usadas para criar o projeto e **não são mais necessárias. Estão
aqui apenas como documentação**.

Instale o gerenciador de pacotes `uv` um substituto pro pip e outros utilitários do Python.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Supondo que o diretório corrente seja: `$HOME/dev/claude/python/`

```bash
# Desativa o Virtual Environment atual. O comando uv add criará automaticamente um ambiente Virtual
deactivate
# Crie o projeto de modulo Python
uv init psql-catalog --python 3.12 # Escolha a versão do Python
# Modifica o diretório corrente no Terminal
cd psql-catalog
uv add psycopg2-binary rich typer tabulate
uv add --dev pytest pytest-cov black isort flake8 mypy
uv pip install -e .
```

## License

MIT License
