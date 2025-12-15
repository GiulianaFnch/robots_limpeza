# Arquivo: main.py
import sys
import database as db  
from models.robot import Robot
from models.tarefa import Tarefa

def limpar_tela():
    """Função auxiliar para limpar o terminal (opcional, mas fica bonito)"""
    print("\n" * 50)

def exibir_menu():
    print("="*40)
    print("   SISTEMA DE GESTÃO DE ROBOTS - ISLA")
    print("="*40)
    print("\n--- GESTÃO DE DADOS ---")
    print("1. Adicionar Novo Robot")    # [cite: 14]
    print("2. Criar Nova Tarefa")       # [cite: 15]
    print("3. Listar Todos os Robots")  # [cite: 21]
    print("4. Listar Todas as Tarefas") # [cite: 22]
    
    print("\n--- OPERAÇÕES ---")
    print("5. Iniciar Tarefa")  # [cite: 16]
    print("6. Executar Simulação (Passo de Tempo)") # [cite: 5, 49]
    print("7. Concluir/Cancelar Tarefa")    # [cite: 20]
    
    print("\n--- RELATÓRIOS E MAPAS ---")
    print("8. Gerar Mapa de Eficiência")    # [cite: 25]
    print("9. Relatório de Alertas")        # [cite: 26]
    print("10. Limpar tela")   

    print("\n--- MANUTENÇÃO ---")
    print("11. Excluir Robot")
    print("12. Excluir Tarefa")
    
    print("\n0. Sair")
    print("="*40)

def main():
    db.inicializar_bd()
    
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("\n>> Adicionar Novo Robot")

            # Escolha do modelo
            modelos = {
                '1': 'Aspirador',
                '2': 'Lavador de Chão',
                '3': 'Híbrido'
            }

            print("Escolha o modelo do robot:")
            for k, v in modelos.items():
                print(f"{k}. {v}")

            modelo_escolhido = None
            while modelo_escolhido is None:
                opc_modelo = input("Opção de modelo: ")
                if opc_modelo in modelos:
                    modelo_escolhido = modelos[opc_modelo]
                else:
                    print("Opção inválida. Tente novamente.")

            # Escolha da localização
            locais = {
                '1': 'Receção',
                '2': 'Escritório A',
                '3': 'Escritório B',
                '4': 'Sala de Reuniões',
                '5': 'Armazém'
            }

            print("\nEscolha a localização inicial do robot:")
            for k, v in locais.items():
                print(f"{k}. {v}")

            local_escolhido = None
            while local_escolhido is None:
                opc_local = input("Opção de localização: ")
                if opc_local in locais:
                    local_escolhido = locais[opc_local]
                else:
                    print("Opção inválida. Tente novamente.")

            # Criação do robot com valores padrão
            robot = Robot(
                id_robot=None,
                modelo=modelo_escolhido,
                estado="Estacionado",
                bateria=100,
                deposito=0,
                localizacao=local_escolhido,
                tarefa_atual=None
            )

            db.adicionar_robot_bd(robot)
            input("\nPressione ENTER para continuar...")

        elif opcao == '2':
            # Lógica para criar tarefa
            print("\n>> Nova Tarefa de Limpeza")
            tipo = input("Tipo (Aspiração/Lavagem): ")
            area = input("Nome da Área: ")
            
            tarefa = Tarefa(None, tipo, area)
            db.adicionar_tarefa_bd(tarefa)
            input("\nPressione ENTER para continuar...")

        elif opcao == '3':
            print("\n>> Lista de Robots da Frota")
            robots = db.listar_robots_bd()
            if robots:
                for robot in robots:
                    print(robot)
            else:
                print("Nenhum robot encontrado na frota.")
            input("\nPressione ENTER para continuar...")

        elif opcao == '4':
            print("\n>> Lista de Tarefas Pendentes e em Curso")
            tarefas = db.listar_tarefas_bd()
            if tarefas:
                for tarefa in tarefas:
                    print(tarefa)
            else:
                print("Nenhuma tarefa encontrada.")
            input("\nPressione ENTER para continuar...")

        elif opcao == '5':
            print("\n>> Iniciar Tarefa")
            # lista tarefas pendentes
            
            # Lista robots disponíveis onde: 
            #  robot.pode_trabalhar() == true
            #  tipo limpeza bate com o modelo do robot (aspiração - aspirador)
            
            # Seleciona robot 
            
            # Simulação -> imprementar depois
            # Confirmação (y/n)
            
            # if tarefa_objeto.atribuir_robot(id_robot) == true: -> vai verificar se self.estado != "Pendente"
            # se true, atribui o id do robot ao objeto tarefa com sucesso
            # db.atribuir_tarefa_robot(id_robot, id_tarefa)  -> só depois de tudo verificado, vai atualizar na base de dados
            
            # print ("Sucesso! Robot {id_robot} está a trabalhar...")
            
            # podemos fazer por exemplo:
            # input("Pressione 0 para sair ou 1 para monitorar estado do robot: ")
            # se 1, vai mostrar o robot em progresso na tarefa,
            
            input("\nPressione ENTER para continuar...")

        elif opcao == '6':
            print("\n>> Simulando funcionamento do sistema...")
            # Aqui chamaremos a função de simulação que desconta bateria
            print("... Baterias atualizadas e depósitos a encher ...")
            input("\nPressione ENTER para continuar...")

        elif opcao == '0':
            print("A encerrar sistema...")
            break

        elif opcao == '10':
            limpar_tela()

        elif opcao == '11':  # EXCLUIR ROBOT
            print("\n>> EXCLUIR ROBOT")
            robots = db.listar_robots_bd()
            if not robots:
                print("Nenhum robot encontrado na frota.")
                input("Pressione ENTER para continuar...")
                continue

            print("Lista de Robots da Frota:")
            for robot in robots:
                print(robot)

            print("\nDigite 0 para cancelar.")
            try:
                id_robot = int(input("ID do Robot a excluir: "))
            except ValueError:
                print("ID inválido.")
                input("Pressione ENTER para continuar...")
                continue

            if id_robot == 0:
                print("Operação cancelada.")
                input("Pressione ENTER para continuar...")
                continue

            db.remover_robot_db(id_robot)
            input("Pressione ENTER para continuar...")


        elif opcao == '12':  # EXCLUIR TAREFA
            print("\n>> EXCLUIR TAREFA")
            tarefas = db.listar_tarefas_bd()
            if not tarefas:
                print("Nenhuma tarefa encontrada.")
                input("Pressione ENTER para continuar...")
                continue

            print("Lista de Tarefas:")
            for tarefa in tarefas:
                print(tarefa)

            print("\nDigite 0 para cancelar.")
            try:
                id_tarefa = int(input("ID da Tarefa a excluir: "))
            except ValueError:
                print("ID inválido.")
                input("Pressione ENTER para continuar...")
                continue

            if id_tarefa == 0:
                print("Operação cancelada.")
                input("Pressione ENTER para continuar...")
                continue

            db.remover_tarefa_bd(id_tarefa)
            input("Pressione ENTER para continuar...")
            
        elif opcao == '0':
            print("A encerrar sistema...")
            break
            

            
if __name__ == "__main__":
    main()
