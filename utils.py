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
from plotly.subplots import make_subplots
import plotly.graph_objects as go


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
        log.exception(f"[ERROR-UTILS] Erro de Tipo de valor: {e}")

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

        table_format = f"\nTABELA {name_table.upper()}:\n{dataframe__}\n\nTotal: R$ {total:.2f} \nMédia: R$ {media:.2f} \nMínimo [{label_min}: R$ {minimo:.2f}] \nMáximo: [{label_max}: R$ {maximo:.2f}]".replace(".", ",")
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
            log.exception(f"[ERRO-UTILS-ATUALIZACAO]: {e}")
    elif quest_edit == "1":
        try:
            table = Table(name_db, name_table)
            table.edit_value(input_id, input_value)
            log.info(f"[UTILS] Valores atualizados do {id_} para {input_value}")

            back_to_menu("volte")
        except ValueError as e:
            log.exception(f"[ERRO-UTILS-ATUALIZACAO]: {e}")

def insert_data(name_db, name_table, description, validate: str | None, value__, observation: str | None):
    try:
        df_table = Table(name_db, name_table)
        df_table.insert_payments(description, validate, value__, observation)
        log.info(f"[UTILS] dados inseridos na tabela {name_table}")

        back_to_menu("volte")

    except DatabaseError as e:
        log.exception(f"[ERRO-UTILS-INSERCAO]: {e}")

def delete_data(name_db, name_table, value__):  
    try:
        table = Table(name_db, name_table)
        table.delete_line(value__)
        print(f"\nItem {value__} deletado com sucesso\n")
        log.info(f"[UTILS] {value__} deletado com sucesso")

        back_to_menu("volte")

    except DatabaseError as e:
        log.exception(f"[ERRO-UTILS-DELETE]: {e}")


def query_all_tables(database__):
    try:
        conn = sqlite3.connect(database__)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        tables = cursor.fetchall()
        tables_names = [table for table in tables if not "sqlite_sequence" in table]
        columns_name = ["Tabelas"]
        df = pd.DataFrame(data=tables_names, columns=columns_name)

        return df
        
    except OperationalError as e:
        log.exception(f"[ERRO-UTILS-SHOWTABELAS] Erro Operacional: {e}")

def show_tables(database__):
    query_all = query_all_tables(database__)
    headler = f"""\n
▗▄▄▄▖▗▄▖ ▗▄▄▖ ▗▄▄▄▖▗▖    ▗▄▖  ▗▄▄▖    ▗▄▄▄  ▗▄▖     ▗▄▄▖ ▗▄▄▄ 
  █ ▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌   ▐▌ ▐▌▐▌       ▐▌  █▐▌ ▐▌    ▐▌ ▐▌▐▌  █
  █ ▐▛▀▜▌▐▛▀▚▖▐▛▀▀▘▐▌   ▐▛▀▜▌ ▝▀▚▖    ▐▌  █▐▌ ▐▌    ▐▛▀▚▖▐▌  █
  █ ▐▌ ▐▌▐▙▄▞▘▐▙▄▄▖▐▙▄▄▖▐▌ ▐▌▗▄▄▞▘    ▐▙▄▄▀▝▚▄▞▘    ▐▙▄▞▘▐▙▄▄▀
                                                              
                                                              
\n--> {database__.upper()[:22]}:\n\n{query_all}\n
"""
    print(headler)

def view_menu(input_table):
    print(f"""
                \n
▗▖  ▗▖ ▗▄▖ ▗▖  ▗▖▗▄▄▄▖▗▄▄▖ ▗▖ ▗▖▗▖   ▗▄▄▄▖     ▗▄▖  ▗▄▄▖    ▗▄▄▄  ▗▄▖ ▗▄▄▄  ▗▄▖  ▗▄▄▖
▐▛▚▞▜▌▐▌ ▐▌▐▛▚▖▐▌  █  ▐▌ ▐▌▐▌ ▐▌▐▌   ▐▌       ▐▌ ▐▌▐▌       ▐▌  █▐▌ ▐▌▐▌  █▐▌ ▐▌▐▌   
▐▌  ▐▌▐▛▀▜▌▐▌ ▝▜▌  █  ▐▛▀▘ ▐▌ ▐▌▐▌   ▐▛▀▀▘    ▐▌ ▐▌ ▝▀▚▖    ▐▌  █▐▛▀▜▌▐▌  █▐▌ ▐▌ ▝▀▚▖
▐▌  ▐▌▐▌ ▐▌▐▌  ▐▌▗▄█▄▖▐▌   ▝▚▄▞▘▐▙▄▄▖▐▙▄▄▖    ▝▚▄▞▘▗▄▄▞▘    ▐▙▄▄▀▐▌ ▐▌▐▙▄▄▀▝▚▄▞▘▗▄▄▞▘                                                                             
                                                                                                                                                         
                \n==> [{input_table.upper()}] <==\n
                \n[1] - Visualizar Tabela
                \n[2] - Inserir Dados
                \n[3] - Atualizar Tabela
                \n[4] - Estatísticas
                \n[5] - Deletar Conta ou Recebimento
                \n[6] - Alternar de Tabela
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

def analyze_data(name_db, name_table):
    try:
        conn = sqlite3.connect(name_db)
        df = pd.read_sql(f"SELECT * FROM {name_table}", conn)

        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "bar"}, {"type": "barpolar"}],
                [{"type": "pie"}, {"type": "scatter3d"}]],
                subplot_titles=["Valores Totais", "",
                                "Percentual %", ""]
        )

        fig.add_trace(go.Bar(y=df["valor"], text=df["descricao"]),
                    row=1, col=1)

        fig.add_trace(go.Barpolar(theta=df["descricao"], r=df["pago"]),
                    row=1, col=2)

        fig.add_trace(go.Pie(values=df["valor"], text=df["descricao"]),
                    row=2, col=1)

        fig.add_trace(go.Scatter3d(x=[2, 3, 1], y=[0, 0, 0],
                                z=[0.5, 1, 2], mode="lines+markers+text"),
                    row=2, col=2)

        fig.update_layout(height=1000, width=1500, showlegend=True)

        log.info("SubPlots Gerados")

        return fig.show()

    except ValueError as e:
        log.error(f"[UTILS] - Erro ao gerar gráfico {e}")


def copy_data_table(database, table_1, table_2):
    if not table_1 or table_2:
        return None

    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        execute = cursor.execute(f"""
        INSERT INTO {table_2} (descricao, vencimento, valor) VALUES (?, ?, ?) 
        SELECT descricao, vencimento, valor FROM {table_1};
""")

        return execute, log.info(f"[UTILS] DADOS DE {table_1} COPIADOS PARA {table_2}")

    except ValueError as e:
        log.error(f"[UTILS] - Erro de Valor {e}")