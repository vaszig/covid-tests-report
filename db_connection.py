import os
import contextlib

import psycopg2


@contextlib.contextmanager
def get_psql_conn():
    """
    Context manager to automatically close DB connection. 
    We retrieve credentials from environment variables.
    """
    conn = psycopg2.connect(
            host = os.environ.get('POSTGRES_HOST'),
            database = os.environ.get('POSTGRES_DB'),
            user = os.environ.get('POSTGRES_USER'),
            password = os.environ.get('POSTGRES_PASS'),
        )
    try:
        yield conn
    finally:
        conn.close()
