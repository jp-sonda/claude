# Contributing to this project

Firstly, thanks for your interest in contributing! I hope that this will be a
pleasant experience for you, and that you will return to continue
contributing.

## Features

- **Schema Navigation**: List all schemas in your PostgreSQL database
- **Table Listing**: View all tables within a specific schema
- **Table Structure**: Detailed column information including data types, nullability, defaults
- **Index Information**: View all indexes for tables including unique and primary key indexes
- **Integrity Constraints**: Display all integrity constraints including:
  - Primary Key constraints
  - Foreign Key constraints with referential actions (ON UPDATE/ON DELETE)
  - Unique constraints
  - Check constraints with their conditions
- **Interactive Mode**: Command-line interface for easy database exploration
- **Rich Output**: Beautiful, formatted tables using Rich library
- **Fast Performance**: Built with UV package manager for optimal speed

## Installation

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

### Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd psql-catalog
```

2. Set up the project (this will create a virtual environment and install all dependencies):

```bash
uv sync
```

3. Activate the virtual environment:

```bash
# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Alternative: Direct execution with uv

You can also run the tool directly without manually activating the virtual environment:

```bash
uv run psql-catalog --help
```

## Usage

### List schemas

```bash
psql-catalog schemas --db "postgresql://user:password@localhost:5432/database"
```

### List tables in a schema

```bash
psql-catalog tables --schema public --db "postgresql://user:password@localhost:5432/database"
```

### Describe a table

```bash
# Basic table description
psql-catalog describe users --schema public --db "postgresql://user:password@localhost:5432/database"

# Include integrity constraints (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK)
psql-catalog describe users --schema public --constraints --db "postgresql://user:password@localhost:5432/database"

# Short form with constraints
psql-catalog describe users -s public -c --db "postgresql://user:password@localhost:5432/database"
```

### Interactive mode

```bash
psql-catalog interactive
```

## Development

### Install development dependencies

Development dependencies are automatically installed with `uv sync`.

### Running tests

```bash
uv run pytest
```

### Code formatting

```bash
# Format code
uv run black src/ tests/

# Sort imports
uv run isort src/ tests/

# Lint code
uv run flake8 src/ tests/

# Type checking
uv run mypy src/
```

### Adding new dependencies

```bash
# Add runtime dependency
uv add package-name

# Add development dependency
uv add --dev package-name
```

## Project Structure

```
psql-catalog/
├── src/
│   └── psql_catalog/
│       ├── __init__.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── pyproject.toml
├── .python-version
├── uv.lock
└── README.md
```

## Connection String Format

The PostgreSQL connection string should follow this format:

```
postgresql://username:password@host:port/database
```

Example:

```
postgresql://myuser:mypassword@localhost:5432/mydatabase
```

## Environment Variables

You can also set connection parameters via environment variables:

- `PGHOST`
- `PGPORT`
- `PGDATABASE`
- `PGUSER`
- `PGPASSWORD`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request
