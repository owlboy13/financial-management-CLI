from pathlib import Path
from utils import create_table__, view_table, insert_data, update_data
from utils import delete_data, view_menu, show_tables, present_flow_finance
import datetime

BASE_DIR = Path(__file__).parent
DATABASE = "gestao_financeira_2026.db"
DATE_NOW = datetime.datetime.now()
FORMAT_DATE_NOW = datetime.datetime.strftime(DATE_NOW, "%d/%m/%Y %H:%M:%S")

def main():

    present_flow_finance()

    quest_create_table = input("Deseja criar uma nova tabela? [SIM] OU [ENTER PARA PULAR] -> ").lower().strip()
    if quest_create_table == 'sim':
        name_table = input(" [NEW] Digite um nome para sua nova tabela: ").lower().strip()
        try:
            create_table__(name_bd=DATABASE, name_table=name_table)
        except ValueError as e:
            print("[MAIN]: Erro ao criar tabela: ", e)
    show_tables(DATABASE)
    input_table = str(input("Digite o nome da tabela que deseja manipular: ")).lower().strip() 

    while True:

        try:

            view_menu()

            options = int(input("\nEscolha sua opção: "))

            default_pago = True
            input_id__ = None

            responses = [1, 2, 3, 4, 5, 6]

            commands = {
                1: lambda: view_table(name_db=DATABASE, name_table=input_table),
                2: lambda: insert_data(name_db=DATABASE, name_table=input_table,
                                    description=input_description,
                                    validate=input_validate,
                                    value__=input_value),
                3: lambda: update_data(name_db=DATABASE, name_table=input_table,
                                    id_=input_id,
                                    pago=default_pago,
                                    data_pagamento=FORMAT_DATE_NOW),
                4: lambda: print('\nestatisticas em breve...\n'),
                5: lambda: delete_data(name_db=DATABASE, name_table=input_table,
                                    value__=input_id__),
            }


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
                input_pago = input("marcar como pago? [sim] ou [não]\n").lower().strip()
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

if __name__ == '__main__':
    main()