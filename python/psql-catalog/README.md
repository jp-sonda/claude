# psql-catalog

Consulte informações sobre o catalogo PostgreSQL dado um schema e as credenciais de acesso.

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

## Exemplo de uso

Depois de configurar o modulo, você poderá usar o seu projeto assim:

Crie uma variavel no ambiente com a String de conexão ao seu Banco de Dados, como no exemplo:

```bash
export DP_PORT=5432
export MY_DB="my_db_name"
export DB_CONN="postgresql://my_user:my_password@my_db_host:$DP_PORT/$MY_DB"
```

```bash
# Listar schemas
psql-catalog schemas --db $DB_CONN

![psql-catalog-01](docs/psql-catalog-01.png docs/)

# Listar tabelas
psql-catalog tables --schema public --db $DB_CONN

# Descrever uma tabela
psql-catalog describe users --schema public --db $DB_CONN

# Modo interativo
psql-catalog interactive
```

## Por que usar o **uv** como gerenciador de pacotes Python ?

Com essa configuração você terá:

- Velocidade: O uv é muito mais rápido que pip/pip-tools
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
