# Arquivo: main.py
import sys
# import database as db  <-- Descomentar quando você criar o database.py
# from models.robot import Robot
# from models.tarefa import Tarefa

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
    
    print("\n0. Sair")
    print("="*40)

def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            # Lógica para adicionar robot
            print("\n>> Adicionar Novo Robot")
            # modelo = input("Modelo (Aspirador/Lavador): ")
            # local = input("Localização Inicial: ")
            # Aqui chamaremos: db.adicionar_robot(modelo, local)
            input("Pressione ENTER para continuar...")

        elif opcao == '2':
            # Lógica para criar tarefa
            print("\n>> Nova Tarefa de Limpeza")
            # tipo = input("Tipo (Aspiração/Lavagem): ")
            # area = input("Nome da Área: ")
            # Aqui chamaremos: db.criar_tarefa(tipo, area)
            input("Pressione ENTER para continuar...")

        elif opcao == '3':
            print("\n>> Lista de Robots da Frota")
            # Aqui chamaremos: db.listar_robots()
            input("Pressione ENTER para continuar...")

        elif opcao == '4':
            print("\n>> Lista de Tarefas Pendentes e em Curso")
            # Aqui chamaremos: db.listar_tarefas()
            input("Pressione ENTER para continuar...")

        elif opcao == '5':
            print("\n>> Atribuir Tarefa")
            # Esta será a parte complexa que faremos juntos
            # 1. Listar robots disponiveis
            # 2. Listar tarefas pendentes
            # 3. Pedir IDs e validar
            input("Pressione ENTER para continuar...")

        elif opcao == '6':
            print("\n>> Simulando funcionamento do sistema...")
            # Aqui chamaremos a função de simulação que desconta bateria
            print("... Baterias atualizadas e depósitos a encher ...")
            input("Pressione ENTER para continuar...")

        elif opcao == '0':
            print("A encerrar sistema...")
            break
            
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()