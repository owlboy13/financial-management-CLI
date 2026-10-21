import sqlite3
import hashlib
import logging
from main import DATABASE, TABLE_ACCOUNT

log = logging.getLogger(__name__)


def authentication(username, password):
    validate = False
    if not username or not password:
        log.error("Precisa adicionar os parametros username e password")
        return None

    password__ = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = f"""
            SELECT username from {TABLE_ACCOUNT} WHERE username= ? AND password= ?
"""

    cursor.execute(query, (username, password__))

    if not cursor.fetchone():
        return log.error("Autenticacao falhou")

    log.info("Autenticado com sucesso")
    validate = True
    return validate