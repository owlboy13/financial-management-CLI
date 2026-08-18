"""
Funções para manipular os dados do BD e tornar com 
melhor visualização e manipulação usando pandas e plotly express e matplotlib:

RECRIAR CRUD 
criar tabelas por mes/ano

    - Gastos
    - Ganhos

inserir dados e escolher o a tabela 

    - cada tabela tem um total 

ler tabela e consultar graficos

    - duas funcoes
        - uma gera a tabela no cli com o total;
        - outra gera graficos para analise;
    
editar valores ja adicionados e adicionar novos atributos

    - duas funcoes
        - uma edita valores ja adicionados (descricao, valor, vencimento, pago);

        - outra adiciona novos atributos caso seja necessario;


excluir valores

"""
from database import DataBase, Table
import pandas as pd
import sqlite3
from sqlite3 import OperationalError 


def back_to_menu():
    menu = input("\naperte [ENTER] e volte para o menu...")
    return menu

def create_table__(name_bd, name_table):
    if not name_bd:
        return None
    try:
        table = Table(name_bd, name_table)
        table.create_table()
        print(f"[UTILS] Tabela {name_table} criada com sucesso")

        back_to_menu()

    except Exception as e:
        print(e)

def view_table(name_db, name_table):
    if not name_db or not name_table:
        print("[banco ou tabela não existem]")
        return None
    try:
        conn = sqlite3.connect(name_db)
        df = pd.read_sql(f"SELECT * FROM {name_table}", conn)
        total = df['valor'].sum()
        dataframe__ = pd.DataFrame(df)
        print(f"\nTabela {name_table}:\n{dataframe__}\n\nTotal: R$ {total:.2f}".replace(".", ","))
        print("=="*40)

        back_to_menu()

    except Exception as e:
        print("[ERRO-UTILS-LEITURA]: ", e)
    return None

def insert_data(name_db, name_table, description, validate, value__):
    try:
        df_table = Table(name_db, name_table)
        print(f"[UTILS] dados inseridos na tabela {name_table}")

        df_table.insert(description, validate, value__)
    
        back_to_menu()

    except Exception as e:
        print("[ERRO-UTILS-INSERCAO]: ", e)


def update_data(name_db, name_table, id_, pago, data_pagamento):
    if not id_:
        return None
    try:
        table = Table(name_db, name_table)
        table.update(id_, pago, data_pagamento)
        print(f"[UTILS] Dados atualizados do {id_} como {pago}")

        input("\naperte [ENTER] e volte para o menu...\n")
    except Exception as e:
        print("[ERRO-UTILS-ATUALIZACAO]: ", e)

def add_column_table(name_db, name_table, column_name, datatype__, count_caracteres: str | None):
    """
        Função ainda não definidade e não está funcionando
    
    """
    try:
        table = Table(name_db, name_table)
        table.alter_table(column_name, datatype__, count_caracteres)
        print(f"[UTILS] Coluna {column_name} adicionada com sucesso")

        back_to_menu()

    except OperationalError as e:
        print("[ERRO-UTILS] Erro Operacional: ", e)

    except Exception as e:
        print("[ERRO-UTILS] Erro ao adicionar coluna: ", e)

def delete_data(name_db, name_table, value__):  
    try:
        table = Table(name_db, name_table)
        table.delete_line(value__)
        print(f"[UTILS] {value__} deletado com sucesso")

        back_to_menu()

    except Exception as e:
        print("[ERRO-UTILS-DELETE]: ", e)


def show_tables(database__):
    try:
        conn = sqlite3.connect(database__)
        cursor = conn.cursor()

        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table';")

        tables = cursor.fetchall()
        tables_names = [table[0] for table in tables]

        print(f"\nTabelas do Banco de Dados {database__}:\n")

        count__ = 0

        for table_name in tables_names:
            count__ = count__ + 1
            print(f"[{count__}] - {table_name}\n")


        return None
        
    except OperationalError as e:
        print(f"[ERRO-UTILS-SHOWTABELAS] Erro Operacional: {e}")

def view_menu():
    print("""
                \n  MANIPULE OS DADOS:\n
                \n[1] - Criar Nova Tabela
                \n[2] - Visualizar Tabela
                \n[3] - Inserir Dados
                \n[4] - Atualizar Tabela
                \n[5] - Estatísticas
                \n[6] - Deletar Conta ou Recebimento
                \n[0] - Sair
    """)

def present_flow_finance():
    header = """
    █████ █      ███  █   █ █████ ███ █   █  ███  █   █  ███  █████ 
    █     █     █   █ █   █ █      █  ██  █ █   █ ██  █ █     █     
    ████  █     █   █ █ █ █ ████   █  █ █ █ █████ █ █ █ █     ████  
    █     █     █   █ ██ ██ █      █  █  ██ █   █ █  ██ █     █     
    █     █████  ███  █   █ █     ███ █   █ █   █ █   █  ███  █████ 

    """
    print("=="*40)
    print(f"\n{header}")
    print("=="*40)

    input("\nAperte [ENTER] para abrir o menu com opções...")


if __name__ == '__main__':
    # create_table__("teste.db", "GanhosTeste")
    # create_table__("teste.db", "GastosTeste")
    # insert_data("teste.db", "GanhosTeste", "Manutencao Laptop", "29/07/2026", 80)
    # insert_data("teste.db", "GastosTeste", "Das MEI", "29/08/2026", 80.66)
    # insert_data("teste.db", "GanhosTeste", "Venda de Software", "29/07/2026", 1900)
    # insert_data("teste.db", "GastosTeste", "Conta de Luz", "29/08/2026", 300.58)
    # update_data("teste.db", "GastosTeste", "1", True, "01/08/2026")
    
    view_table("teste.db", "GanhosTeste")
    view_table("teste.db", "GastosTeste")
    show_tables("teste.db")




