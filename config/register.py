"""
Sistema de login e senha para acessar banco de dados e o flowfinance

username: str 
password: str >> hashlib
save: SQLITE3

"""

import hashlib
from dotenv import load_dotenv
import logging
import pandas as pd
import sqlite3
from sqlite3 import ProgrammingError

load_dotenv()

log = logging.getLogger(__name__)

class Register:

    def __init__(self, username, password, database, table, fullname) -> None:
        self.fullname = fullname
        self.username = username
        self.password = password
        self.database = database
        self.table = table

    def hash_password(self, password__) -> str:
        return hashlib.sha256(password__.encode()).hexdigest()

    def create_table_user(self):
        query = f"""
                CREATE TABLE IF NOT EXISTS {self.table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_completo TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    confirm_password TEXT NOT NULL,
                    status BOOLEAN DEFAULT TRUE)"""
        try:
            table = sqlite3.connect(self.database)
            table.cursor()
            table.execute(query)
            log.info(f"[CONTROLLER-ACCOUNT] - TABELA {self.table} criada com sucesso!")

        except ValueError as e:
            log.exception(f"[CONTROLLER-ACCOUNT] - {e}")

        finally:
            table.close()

    def create_username(self):
        query = f"""
                INSERT INTO {self.table} (nome_completo, username, password, confirm_password) VALUES (?, ?, ?, ?);
"""

        cripto_password = self.hash_password(self.password)

        cripto_password_2 = self.hash_password(self.password)

        if cripto_password != cripto_password_2:
            log.error("[CONTROLLER-ACCOUNT] - Senhas precisam estar iguais")
            return None
        try:
            db = sqlite3.connect(self.database)
            db.cursor()
            db.execute(query, (self.fullname, self.username, cripto_password, cripto_password_2))

            db.commit()

            log.info("[CONTROLLER-ACCOUNT] - UserName criado com sucesso")
            
        except ValueError as e:
            log.exception(f"[CONTROLLER-ACCOUNT] - {e}")

        except ProgrammingError as e:
            log.exception(f"[CONTROLLER-ACCOUNT] - {e}")

        finally:
            db.close()

        return None

    def view_table_users(database, table):
        try:
            query = f"""
                SELECT * FROM {table}

    """
            table = sqlite3.connect(database)

            table.cursor()

            if not table:
                return None

            for row in table.execute(query):
                print(row)

            table.commit()
            log.info("[CONTROLLER-ACCOUNT] - Conta visualizada")

        except ValueError as e:
            log.error(f"[CONTROLLER-ACCOUNT] -  {e}")

        finally:
            table.close()
