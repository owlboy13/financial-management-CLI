from pathlib import Path
from utils import create_table__, view_table, insert_data, update_data, kpis_table
from utils import delete_data, view_menu, show_tables, present_flow_finance, query_all_tables
import datetime
import logging

log = logging.getLogger(__name__)

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
            log.error("[MAIN]: Erro ao criar tabela: %s", e)
    show_tables(DATABASE)
    input_number_table = input("Digite o número da tabela que deseja manipular: ")

    try:
        
        input_table = query_all_tables(DATABASE).loc[int(input_number_table)].item()

    except ValueError as e:
        log.warning(f"[MAIN] Input Table precisa ser um valor inteiro: {e}")
        log.info("RE-opening FlowFinance")
        main()
        
    except KeyError as e:
        log.warning(f"[MAIN] Input Table precisa ser um valor positivo: {e}")
        log.info("RE-opening FlowFinance")
        main()


    while True:

        try:

            view_menu(input_table)

            options = int(input("\nEscolha sua opção: "))

            default_pago = True
            input_id__ = None
            input_value = None

            responses = [1, 2, 3, 4, 5, 6]

            commands = {
                1: lambda: view_table(name_db=DATABASE, name_table=input_table, 
                                      function=kpis_table),
                2: lambda: insert_data(name_db=DATABASE, name_table=input_table,
                                    description=input_description,
                                    validate=input_validate,
                                    value__=input_value),
                3: lambda: update_data(name_db=DATABASE, name_table=input_table,
                                    id_=input_id,
                                    pago=default_pago,
                                    data_pagamento=FORMAT_DATE_NOW,
                                    quest_edit=quest_edit,
                                    input_id=input_id,
                                    input_value=input_value),
                4: lambda: print('\nestatisticas em breve...\n'),
                5: lambda: delete_data(name_db=DATABASE, name_table=input_table,
                                    value__=input_id__),
                6: lambda: show_tables(DATABASE),
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
                print("[1] - Editar Valor\n[2] - Marcar como Pago\n")
                quest_edit = input("Digite o número da operacao que deseja executar: ").lower().strip()
                if quest_edit == "2":
                    input_id = input("digite o id da conta: \n")
                    input_pago = input("marcar como pago? [sim] ou [não]\n").lower().strip()
                    if input_pago != "sim" and input_pago != "s":
                        default_pago = False
                elif quest_edit == "1":
                    input_value = float(input("Digite o valor que deseja adicionar: \n").replace(",", "."))
                    input_id = input("...e qual o [ID] da conta para alterar? \n")

            if options == responses[4]:
                print("""
                    \nVisualize o [id] que deseja apagar\n
    """)
                input_id__ = input("\ndigite o [id] que deseja apagar: \n")
            if options == responses[5]:

                show_tables(DATABASE)
                
                input_number_table = int(input("Digite o número da tabela que deseja manipular: "))

                if not isinstance(input_number_table, int):
                        raise TypeError("Escolha um valor inteiro e positivo...")
                
                input_table = query_all_tables(DATABASE).loc[input_number_table].item()

            if options in commands:
                command = commands[options]

            if options == 0:
                print("\nSaindo do FlowFinance...")
                log.info("Leaving FlowFinance")
                break

            command()

        except ValueError as e:
            log.error(f"[MAIN] Erro de Valor: {e}")

        except AttributeError as e:
            log.error(f"[MAIN] Erro de Atributo: {e}")

if __name__ == '__main__':
    main()