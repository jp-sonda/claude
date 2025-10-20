import sys
from pathlib import Path
import time
import psycopg
from pgvector.psycopg import register_vector
from sqlalchemy import create_engine, text
import numpy as np

