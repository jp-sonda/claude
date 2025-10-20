import marimo

__generated_with = "0.17.0"
app = marimo.App(
    width="medium",
    app_title="Consultas por similaridade",
    auto_download=["ipynb"],
)


@app.cell
def _():
    import sys
    from pathlib import Path
    import time
    import psycopg
    from pgvector.psycopg import register_vector
    from sqlalchemy import create_engine, text
    import numpy as np

    import marimo as mo
    # Adiciona o diretório ao path para importar o módulo run_sql
    sys.path.insert(0, str(Path(__file__).parent))
    return


@app.cell
def _():
    DB_CONFIG = {
        "host": "localhost",
        "port": 5434,
        "dbname": "postgres",  # "pm_rag",
        "user": "postgres",  # "postgres",
        "password": "allsecret",
    }
    return (DB_CONFIG,)


@app.cell
def _(DB_CONFIG):
    print(f"Conectando ao Postgres em {DB_CONFIG['host']}")
    return


@app.cell
def _():

    from run_sql import (
        get_connection_string, 
        get_sqlalchemy_connection_string, 
        create_psycopg_connection, 
        create_sqlalchemy_engine, 
        test_similarity_search,
    )

    print(f"sqlalchemy_connection_string = {get_sqlalchemy_connection_string()}")

    return (test_similarity_search,)


@app.cell
def _(test_similarity_search):
    test_similarity_search()
    return


if __name__ == "__main__":
    app.run()
