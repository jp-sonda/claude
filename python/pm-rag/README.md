# pm rag

Plant Mantainance rag

[![PyPI - Version](https://img.shields.io/pypi/v/pm-rag.svg)](https://pypi.org/project/pm-rag)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pm-rag.svg)](https://pypi.org/project/pm-rag)

---

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
dectivate # Desativa Virtual Environment, caso aja algum ativo.
which python3 # Verifica se está apontando paara o Python original do Sistema
python3 -m venv .venv # Cria o novo Virtual Environment, caso ainda não tenha feito isso
source .venv/bin/activate # Ativa o Virtual Environment do projeto
which python3 # Verifica se está apontando paara o Python do Virtual Environment
python3 -m pip install -e .  # Instala a Aplicação.
```

## Exemplo de uso

Depois de configurar instalar o modulo, você poderá usar o seu projeto assim:

Crie uma variavel no ambiente com a String de conexão ao seu Banco de Dados, como no exemplo veja:

```bash
# Construa a variável DB_CONN com a URL de acesso ao database.
export DP_PORT=5434
export MY_DB="postgres"
export DB_CONN_RAG="postgresql://postgres:allsecret@localhost:$DP_PORT/$MY_DB"
```

## License

`pm-rag` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
