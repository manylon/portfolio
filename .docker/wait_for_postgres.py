import os
import time
import logging
import psycopg2
from psycopg2 import OperationalError


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

TIMEOUT = 30
INTERVAL = 2


def wait_for_postgres():
    start_time = time.time()
    while True:
        try:
            connection = psycopg2.connect(
                host=os.environ.get("POSTGRES_HOST"),
                port=os.environ.get('POSTGRES_PORT', default='5432'),
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD'),
                dbname=os.environ.get('POSTGRES_DB'),
                sslmode=os.environ.get("POSTGRES_SSLMODE"),
                connect_timeout=TIMEOUT,
            )
            connection.close()
            logger.info("Postgres is alive and accepting connections.")
            return True
        except OperationalError as e:
            if time.time() - start_time > TIMEOUT:
                logger.error(
                    f"Timeout reached. Postgres is not available.\n{type(e).__name__}\n{e}")
                return False
            logger.info("Waiting for Postgres to be available...")
            time.sleep(INTERVAL)


wait_for_postgres()
