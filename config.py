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

load_dotenv()

log = logging.getLogger(__name__)

class ControllerAccount:

    def __init__(self, username, password, database):
        self.username = username
        self.password = password
        self.database = database
        self.connected:bool =  False

    def hash_password(self):
        return hashlib.sha256(self.password.encode()).hexdigest()

    def create_user(self):
        ...

    def validation_account(self):
        ...





