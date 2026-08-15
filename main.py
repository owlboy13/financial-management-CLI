from pathlib import Path
from utils import create_table__, view_table, insert_data, update_data, delete_data, view_menu, show_tables
import datetime

BASE_DIR = Path(__file__).parent
DATABASE = "teste.db"
DATE_NOW = datetime.datetime.now()

while True:

    try:

        menu__ = view_menu()

        options = int(input("\nEscolha sua opção: "))

        default_pago = True

        input_id__ = None
        name_table = None

        responses = [1, 2, 3, 4, 5, 6]


        if options == responses[0]:
            name_table = input("Digite um nome para sua nova tabela: ").lower()


        commands = {
            1: lambda: create_table__(name_bd=DATABASE, name_table=name_table),
            2: lambda: view_table(name_db=DATABASE, name_table=input_table),
            3: lambda: insert_data(name_db=DATABASE, name_table=input_table,
                                description=input_description,
                                validate=input_validate,
                                value__=input_value),
            4: lambda: update_data(name_db=DATABASE, name_table=input_table,
                                id_=input_id,
                                pago=default_pago,
                                data_pagamento=DATE_NOW),
            5: lambda: print('\nestatisticas em breve...\n'),
            6: lambda: delete_data(name_db=DATABASE, name_table=input_table,
                                value__=input_id__),
        }

        # Removendo indice 0 (zero) da lista de opcoes
        responses.pop(0)

        if options in responses:
            show_tables__ = show_tables(DATABASE)
            input_table = str(input("Digite o nome da tabela: "))
            if options == responses[1]:
                print("""
                        \nMenu de Insercao\n 
""")
                input_description = input("descreva a conta a pagar ou receber: \n")
                input_validate = input("digite a data de vencimento ou recebimento: \n")
                input_value = float(input("digite o valor: (R$) \n").replace(",", "."))

            if options == responses[2]:
                print("""
                    \nMenu de Atualizacao\n
""")
                input_id = input("digite o id da conta: \n")
                input_pago = input("marcar como pago? [sim] ou [não]\n").lower()
                if input_pago != "sim" and input_pago != "s":
                    default_pago = False

            if options == responses[4]:
                print("""
                    \nVisualize o [id] que deseja apagar\n
""")
                input_id__ = input("\ndigite o [id] que deseja apagar: \n")


        if options in commands:
            command = commands[options]

        if options == 0:
            print("\nSaindo do FlowFinance...")
            break

        command()

    except ValueError as e:
        print(f"[MAIN] Erro de Valor: {e}")

    except AttributeError as e:
        print(f"[MAIN] Erro de Atributo: {e}")

    