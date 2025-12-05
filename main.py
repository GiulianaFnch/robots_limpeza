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
    print("5. Atribuir Tarefa a um Robot")  # [cite: 16]
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
            # Lógica para adicionar robot
            print("\n>> Adicionar Novo Robot")
            modelo = "Aspirador" #  aqui temos que alterar pra ser input() do usuário (ele vai escrever o modelo e localização)
            localizacao = "Sala"

            robot = Robot(None, modelo, localizacao)
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
                id_robot_remover = int(input("Qual robot deseja remover? Pressione 0 pra n remover ")) # mudar de lugar -> opção "remover robot"
                
                if id_robot_remover!=0:
                    db.remover_robot_db(id_robot_remover)
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
            # 1. Nova 2. Existente
            # Salva ID tarefa
            # Lista robots disponíveis pra aquela tarefa
            # Seleciona robot
            # Simulação
            # Confirmação
            
            
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

        elif opcao == '11':  # ← NOVA: Excluir Robot
            print("\n  EXCLUIR ROBOT")
            print(">> Lista de Robots da Frota")
            # Aqui chamaremos: db.listar_robots()
            robot_id = input("ID do Robot a excluir: ")
            # Aqui chamaremos: db.excluir_robot(robot_id)
            print(f"Robot {robot_id} removido da frota!")
            input("Pressione ENTER para continuar...")

        elif opcao == '12':  # ← NOVA: Excluir Tarefa
            print("\n  EXCLUIR TAREFA")
            print(">> Lista de Tarefas")
            # Aqui chamaremos: db.listar_tarefas()
            tarefa_id = input("ID da Tarefa a excluir: ")
            # Aqui chamaremos: db.excluir_tarefa(tarefa_id)
            print(f"Tarefa {tarefa_id} removida!")
            input("Pressione ENTER para continuar...")    
            
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()