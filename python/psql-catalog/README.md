# psql-catalog

Consulte informações sobre o catalogo PostgreSQL dado um schema e as credenciais de acesso.

```bash
uv add psycopg2-binary rich typer tabulate
uv add --dev pytest pytest-cov black isort flake8 mypy
uv pip install -e .
```

## Exemplo de uso

Depois de configur o modulo, você poderá usar o seu projeto assim:

```bash
# Listar schemas
psql-catalog schemas --db "postgresql://user:password@localhost:5432/database"

![psql-catalog-01](docs/psql-catalog-01.png docs/)

# Listar tabelas
psql-catalog tables --schema public --db "postgresql://user:password@localhost:5432/database"

# Descrever uma tabela
psql-catalog describe users --schema public --db "postgresql://user:password@localhost:5432/database"

# Modo interativo
psql-catalog interactive
```

## Por que usar o **uv** como gerenciador de pacotes Python ?

Com essa configuração você terá:

- Velocidade: O uv é muito mais rápido que pip/pip-tools
- Compatibilidade: Mantém a estrutura src/ que você já conhecemos de outros projetos
- Gestão de dependências: Resolve dependências de forma mais eficiente
- Python 3.13+: Suporte nativo para a versão mais recente
- Desenvolvimento: Ferramentas de lint, formatação e testes já configuradas no pyproject.toml

O projeto está pronto para você começar a desenvolver seu navegador de catálogo PostgreSQL!
