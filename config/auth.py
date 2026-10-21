import sqlite3
import hashlib
import logging
from dotenv import load_dotenv
from main import DATABASE, TABLE_ACCOUNT

log = logging.getLogger(__name__)


def authentication(username, password):
    if not username and password:
        log.error("Precisa adicionar os parametros username e password")
        return None

    password = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    query = f"""
            SELECT username from {TABLE_ACCOUNT} WHERE username='{username}' AND password='{password}'
"""

    cursor.execute(query)

    if not cursor.fetchone():
        return log.error("Autenticacao falhou")

    return log.info("Autenticado com sucesso")