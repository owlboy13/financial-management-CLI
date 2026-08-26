from utils import show_tables
from main import DATABASE
import pandas as pd
import sqlite3
from pandas.errors import DatabaseError

input_table = "sadasda"
conn = sqlite3.connect("gestao_financeira_2026.db")
df = pd.read_sql(f"""
                SELECT * FROM {input_table}
""", conn)

print(df)
