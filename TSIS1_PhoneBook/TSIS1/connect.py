from contextlib import contextmanager
import psycopg2
from config import load_config

@contextmanager
def connect():
    conn = psycopg2.connect(**load_config())
    try:
        with conn:
            yield conn
    finally:
        conn.close()
