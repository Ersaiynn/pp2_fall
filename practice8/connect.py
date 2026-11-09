from contextlib import contextmanager
import psycopg2
from config import load_config

@contextmanager
def connect():
    config = load_config()
    conn = psycopg2.connect(**config)

    try:
        with conn:
            yield conn
    finally:
        conn.close()