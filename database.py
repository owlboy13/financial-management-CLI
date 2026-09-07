import sqlite3 as sql
from sqlite3 import OperationalError, ProgrammingError
import logging

log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='./logs/logs.log', encoding='utf-8', level=logging.DEBUG)


class DataBase:
    def __init__(self, name_db):
        self._name_db = name_db
        self.conn = None
        self.cursor = None
        self.connected = False

    @property
    def name_db(self):
        return self._name_db

    def connect(self):
        self.conn = sql.connect(self.name_db)
        self.cursor = self.conn.cursor()
        self.connected = True
        return self.cursor, self.connected
    
    def close(self):
        if self.conn:
            self.conn.close()
            self.connected = False

    def __exit__(self, exc_type, exc, tb):
        self.close()

class Table(DataBase):
    def __init__(self, name_db, name_table):
        super().__init__(name_db)
        self._name_table = name_table

    @property
    def name_table(self):
        return self._name_table
    
    def create_table(self):
        try:
            query = f"""
                    CREATE TABLE IF NOT EXISTS {self.name_table} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        descricao TEXT NOT NULL,
                        vencimento TEXT NOT NULL,
                        valor DECIMAL(10, 2) NOT NULL,
                        pago BOOLEAN DEFAULT FALSE,
                        data_pagamento TEXT DEFAULT NULL,
                        observacao TEXT DEFAULT NULL)"""
            db = DataBase(self.name_db)
            db.connect()
            db.cursor.execute(query)
            db.conn.commit()
            log.info("[DATABASE] Banco de dados conectado e tabela criada com sucesso")
        except TypeError as e:
            log.error("[DATABASE] Erro de tipo de arquivos:", e)
        except AttributeError as e:
            log.error("[DATABASE] Erro de Atributo", e)


    def read_table(self):
        try:
            query = f"""
SELECT * FROM {self.name_table}
"""
            db = DataBase(self.name_db)
            db.connect()
            db.cursor.execute(query)
            all_arrows = db.cursor.fetchall()
            for row in all_arrows:
                print(row)
            db.conn.commit()
        except TypeError as e:
            log.error("[DATABASE] Erro", e)
        except AttributeError as e:
            log.error("[DATABASE] Erro de Atributo", e)

    def insert_payments(self, descricao, vencimento, valor):
        try:
            query = f"""
INSERT INTO {self.name_table} (descricao, vencimento, valor) VALUES (?, ?, ?);
"""
            db = DataBase(self.name_db)
            db.connect()
            db.cursor.execute(query, (descricao, vencimento, valor))
            db.conn.commit()
            db.close()
        except TypeError as e:
            log.error("[DATABASE] Erro de Tipo de dado: ", e)
        except AttributeError as e:
            log.error("[DATABASE] Erro de Atributo: ", e)
        except OperationalError as e:
            log.error("[DATABASE] Erro Operacional: ", e)

    def insert_recept(self, descricao, valor, pago, data_pagamento):
        try:
            query = f"""
INSERT INTO {self.name_table} (descricao, valor, pago, data_pagamento) VALUES (?, ?, ?, ?);
"""
            db = DataBase(self.name_db)
            db.connect()
            db.cursor.execute(query, (descricao, valor, pago, data_pagamento))
            db.conn.commit()
            db.close()
        except TypeError as e:
            log.error("[DATABASE] Erro de Tipo de dado: ", e)
        except AttributeError as e:
            log.error("[DATABASE] Erro de Atributo: ", e)
        except OperationalError as e:
            log.error("[DATABASE] Erro Operacional: ", e)           

    def update_payment(self, id, pago, data_pagamento):
        try:
            query = f"""
                UPDATE {self.name_table} SET pago = ?, data_pagamento = ? WHERE id = ?
"""     
            db = DataBase(self.name_db)
            db.connect()
            db.cursor.execute(query, (pago, data_pagamento, id))
            db.conn.commit()
            db.close()
        except TypeError as e:
            log.error("[DATABASE] Erro de Tipo de dado: ", e)
        except AttributeError as e:
            log.error("[DATABASE] Erro de Atributo: ", e)
        except OperationalError as e:
            log.error("[DATABASE] Erro Operacional: ", e)

    def edit_value(self, id_, value_):
        if value_ == 0 or value_ == None:
            return None
        try:
            query = f"""
                UPDATE {self.name_table} SET valor = ? WHERE id = ?
"""     
            db = DataBase(self.name_db)
            db.connect()
            db.cursor.execute(query, (value_, id_))
            db.conn.commit()
            db.close()
        except ValueError as e:
            log.error("[DATABASE-ERROR-EDITVALUE]: ", e)
        except OperationalError as e:
            log.error("[DATABASE-ERROr-EDITVALUE]: ", e)

        return None

    def alter_table(self, column_name, datatype__, count_caract: str | None):
        """
            Esse método por enquanto é para add new column 
            mas caso haja outra funcao adicionar atraves de condicionais
        """
        try:
            query = f"""
                ALTER TABLE {self.name_table} ADD COLUMN {column_name} {datatype__}({count_caract}) DEFAULT NULL
"""         
            db = DataBase(self.name_table)
            db.connect()
            db.cursor.execute(query)
            db.conn.commit()
            db.close()
            
        except TypeError as e:
            log.error("[DATABASE] Erro de Tipo de dado: ", e)
        except AttributeError as e:
            log.error("[DATABASE] Erro de Atributo: ", e)
        except OperationalError as e:
            log.error("[DATABASE] Erro Operacional: ", e)

    def delete_line(self, value__):
        try:
            query = f"""
                DELETE FROM {self.name_table} WHERE id = ?
"""
            db = DataBase(self.name_db)
            db.connect()
            db.conn.execute(query, value__)
            db.conn.commit()
            db.close()
        except TypeError as e:
            log.error("[DATABASE] Erro de Tipo de dado: ", e)
        except AttributeError as e:
            log.error("[DATABASE] Erro de Atributo: ", e)
        except OperationalError as e:
            log.error("[DATABASE] Erro Operacional: ", e)
        except ProgrammingError as e:
            log.error("[DATABASE] Erro de Programação: ", e)

    def delete_table(self):
        try:
            query = f"""
            DROP TABLE IF EXISTS {self.name_table}
"""
            db = DataBase(self.name_db)
            db.connect()
            db.cursor.execute(query)
            db.conn.commit()
            log.info(f"[QUERY] Tabela {self.name_table} deletada")
        except ValueError as e:
            log.error(f"[ERRO-QUERY-VALOR]: ", e)

        except OperationalError as e:
            log.error(f"[ERRO-QUERY-OPERATIONAL]: ", e)

    def no_payments(self):
        try:
            query = f"""
                SELECT id, descricao, vencimento, valor from {self.name_table} WHERE pago = 0
"""
            db = DataBase("gestao_financeira_2026.db")
            db.connect()
            db.cursor.execute(query)
            all_arrows = db.cursor.fetchall()
            for row in all_arrows:
                print(row)
            db.conn.commit()
        except OperationalError as e:
            log.error(f"[DATABASE-ERRO-NOPAYMENTS-OPERATIONAL: {e}")
        except ValueError as e:
            log.error(f"[DATABASE-ERRO-NOPAYMENTS-VALUE]: {e}")


if __name__ == '__main__':
    table = Table("gestao_financeira_2026.db", "teste"
                  ).delete_table()

