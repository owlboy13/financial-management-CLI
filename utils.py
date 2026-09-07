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
from database import Table
import pandas as pd
import sqlite3
from sqlite3 import OperationalError
import logging
from pandas.errors import DatabaseError

log = logging.getLogger(__name__)

def back_to_menu(keyword):
    menu = input(f"\naperte [ENTER] e {keyword} para o menu...")
    return menu

def create_table__(name_bd, name_table):
    if not name_bd:
        log.error("[ERROR-UTILS] - Tabela Não Existe")
        return None
    try:
        table = Table(name_bd, name_table)
        
        return table.create_table(), back_to_menu("siga")

    except ValueError as e:
        log.exception(e)

    return None

def kpis_table(name_db, name_table):
    try:
        conn = sqlite3.connect(name_db)
        df = pd.read_sql(f"SELECT * FROM {name_table}", conn)
        total = df['valor'].sum()
        media = df['valor'].mean()
        minimo = df['valor'].min()
        label_min = df.loc[df["valor"].idxmin(), "descricao"]
        maximo = df['valor'].max()
        label_max = df.loc[df["valor"].idxmax(), "descricao"]
        dataframe__ = pd.DataFrame(df)

        table_format = f"\nTabela {name_table}:\n{dataframe__}\n\nTotal: R$ {total:.2f} \nMédia: R$ {media:.2f} \nMínimo [{label_min}: R$ {minimo:.2f}] \nMáximo: [{label_max}: R$ {maximo:.2f}]".replace(".", ",")
        log.info("DataFrame formatado")
        return table_format

    except DatabaseError as e:
        log.exception(f"[ERROR-DATABASEERROR-KPIS] {e}")

    except OperationalError as e:
        log.exception(f"[ERROR-OPERATIONAL-KPIS] {e}")
    
    return None

def filter_no_payments(name_db, name_table):
    try:
        query_no_payments = f"""
                SELECT id, descricao, valor, vencimento from {name_table} WHERE pago = 0
    """
        conn = sqlite3.connect(name_db)
        df_no_payments = pd.read_sql(query_no_payments, conn)
        total_pendentes = df_no_payments['valor'].sum()

        total_no_payments = f"\nFiltro {name_table} [PENDENTES]:\n{df_no_payments}\n\nTotal de Pendentes: R$ {total_pendentes:.2f}".replace(".", ",")

        if df_no_payments.empty:

            return f"\n[Todas as contas do {name_table} foram pagas]\n" 

        return total_no_payments

    except OperationalError as e:
        log.exception(f"[OPERATIONALERROR-NOPAYMENTS]: {e}")

    except DatabaseError as e:
        log.exception(f"[DATABASEERROR-NOPAYMENTS] {e}")

    return None

def view_table(name_db, name_table, function):
    kpis = function(name_db, name_table)
    print(kpis)
    print("=="*40)
    back_to_menu("volte")


def update_data(name_db, name_table, id_, pago, data_pagamento,
                quest_edit, input_id, input_value) -> None:
    if quest_edit == "2":
        try:
            table = Table(name_db, name_table)
            table.update_payment(id_, pago, data_pagamento)
            log.info(f"[UTILS] Dados atualizados do {id_} como {pago}")

            back_to_menu("volte")
        except ValueError as e:
            log.exception("[ERRO-UTILS-ATUALIZACAO]: ", e)
    elif quest_edit == "1":
        try:
            table = Table(name_db, name_table)
            table.edit_value(input_id, input_value)
            log.info(f"[UTILS] Valores atualizados do {id_} para {input_value}")

            back_to_menu("volte")
        except ValueError as e:
            log.exception("[ERRO-UTILS-ATUALIZACAO]: ", e)

def insert_data(name_db, name_table, description, validate: str | None, value__):
    try:
        df_table = Table(name_db, name_table)
        df_table.insert_payments(description, validate, value__)
        log.info(f"[UTILS] dados inseridos na tabela {name_table}")

        back_to_menu("volte")

    except DatabaseError as e:
        log.exception("[ERRO-UTILS-INSERCAO]: ", e)

def delete_data(name_db, name_table, value__):  
    try:
        table = Table(name_db, name_table)
        table.delete_line(value__)
        log.info(f"[UTILS] {value__} deletado com sucesso")

        back_to_menu("volte")

    except DatabaseError as e:
        log.exception("[ERRO-UTILS-DELETE]: ", e)


def query_all_tables(database__):
    try:
        conn = sqlite3.connect(database__)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        tables = cursor.fetchall()
        tables_names = [table for table in tables if not "sqlite_sequence" in table]
        columns_name = ["name_table"]
        df = pd.DataFrame(tables_names, columns=columns_name)

        tables__ = f"\nTabelas do [BD] --> {database__}:\n\n{df}\n"

        return tables__
        
    except OperationalError as e:
        log.exception(f"[ERRO-UTILS-SHOWTABELAS] Erro Operacional: {e}")

def show_tables(database__):
    query_all = query_all_tables(database__)
    print(query_all)


def view_menu():
    print("""
                \n ++ MANIPULE OS DADOS ++\n
                \n[1] - Visualizar Tabela
                \n[2] - Inserir Dados
                \n[3] - Atualizar Tabela
                \n[4] - Estatísticas
                \n[5] - Deletar Conta ou Recebimento
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
    log.info("Open FlowFinance")

    input("\nAperte [ENTER] para abrir o menu com opções...")

def analyze_data(dataframe__):
    ...    

if __name__ == '__main__':
    # create_table__("teste.db", "GanhosTeste")
    # create_table__("teste.db", "GastosTeste")
    # insert_data("teste.db", "GanhosTeste", "Manutencao Laptop", "29/07/2026", 80)
    # insert_data("teste.db", "GastosTeste", "Das MEI", "29/08/2026", 80.66)
    # insert_data("teste.db", "GanhosTeste", "Venda de Software", "29/07/2026", 1900)
    # insert_data("teste.db", "GastosTeste", "Conta de Luz", "29/08/2026", 300.58)
    # update_data("teste.db", "GastosTeste", "1", True, "01/08/2026")
    ...