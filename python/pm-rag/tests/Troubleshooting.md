# Troubleshooting

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
