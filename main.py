# Arquivo: main.py
import sys
import time
import database as db  
import config
from models.robot import Robot
from models.tarefa import Tarefa

def limpar_tela():
    """Função auxiliar para limpar o terminal (opcional, mas fica bonito)"""
    print("\n" * 50)

def exibir_menu():
    print("\n" * 10)
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
            # Carrega as áreas disponíveis do config
            locais = {str(i+1): a for i, a in enumerate(config.AREAS_EMPRESA.keys())}

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
            print("\n>> Nova Tarefa de Limpeza")

            # Escolha do tipo de limpeza (ligado aos modelos de robot do enunciado)
            # Carrega os perfis de limpeza do config
            tipos_limpeza = {str(i+1): p for i, p in enumerate(config.PERFIL_LIMPEZA.keys())}

            print("Escolha o tipo de limpeza:")
            for k, v in tipos_limpeza.items():
                print(f"{k}. {v}")

            tipo_escolhido = None
            while tipo_escolhido is None:
                opc_tipo = input("Opção de tipo de limpeza: ")
                if opc_tipo in tipos_limpeza:
                    tipo_escolhido = tipos_limpeza[opc_tipo]
                else:
                    print("Opção inválida. Tente novamente.")

            # Reutiliza as áreas do config para escolher a área da tarefa
            areas = {str(i+1): a for i, a in enumerate(config.AREAS_EMPRESA.keys())}

            print("\nEscolha a área/divisão a ser limpa:")
            for k, v in areas.items():
                print(f"{k}. {v}")

            area_escolhida = None
            while area_escolhida is None:
                opc_area = input("Opção de área/divisão: ")
                if opc_area in areas:
                    area_escolhida = areas[opc_area]
                else:
                    print("Opção inválida. Tente novamente.")

            # Criação da tarefa com estado padrão "Pendente"
            tarefa = Tarefa(
                id_tarefa=None,
                tipo_limpeza=tipo_escolhido,
                area=area_escolhida,
                estado="Pendente"
            )

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
            tarefas = db.listar_tarefas_bd()
            tarefas_pendentes = [t for t in tarefas if t.estado == "Pendente"]

            if not tarefas_pendentes:
                print("Nenhuma tarefa pendente disponível.")
                input("\nPressione ENTER para continuar...")
                continue
            else:
                print("Tarefas Pendentes:")
                for tarefa in tarefas_pendentes:
                    print("ID:", tarefa.id_tarefa, "| Tipo:", tarefa.tipo_limpeza, "| Área:", tarefa.area, "| Estado:", tarefa.estado)
                try:
                    id_tarefa = int(input("\nID da Tarefa a iniciar: "))
                    # Seleciona tarefa
                    tarefa_objeto = next((t for t in tarefas_pendentes if t.id_tarefa == id_tarefa), None)
                    
                    if tarefa_objeto:
                        # filtramos robots baseados nessa tarefa
                        robots_compativeis = []

                        for robot in db.listar_robots_bd():
                            # primeir regra: estado e bateria
                            basico_ok = robot.estado == "Estacionado" and robot.pode_trabalhar()
                            
                            #segunda regra: localização
                            local_ok = robot.localizacao == tarefa_objeto.area

                            # terceira regra: tipo limpeza e modelo
                            if tarefa_objeto.tipo_limpeza == "Aspiração":
                                tipo_ok = robot.modelo in ["Aspirador", "Híbrido"]
                            elif tarefa_objeto.tipo_limpeza == "Lavagem":
                                tipo_ok = robot.modelo in ["Lavador de Chão", "Híbrido"]
                            else:
                                tipo_ok = False

                            if basico_ok and local_ok and tipo_ok:
                                robots_compativeis.append(robot)

                        # mostrar os robots compatíveis
                        if not robots_compativeis:
                            print("Nenhum robot compatível disponível para esta tarefa.")
                            input("\nPressione ENTER para continuar...")
                            continue
                        else:
                            print("\nRobots Compatíveis para a Tarefa:")
                            for robot in robots_compativeis:
                                print("ID:", robot.id_robot, "| Modelo:", robot.modelo, "| Bateria:", robot.bateria, "| Depósito:", robot.deposito, "| Localização:", robot.localizacao)
                            try:
                                id_robot = int(input("ID do Robot a atribuir à tarefa: "))
                            except ValueError:
                                print("ID inválido.")
                                input("\nPressione ENTER para continuar...")
                                continue
                            robot_selecionado = next((r for r in robots_compativeis if r.id_robot == id_robot), None)
                            if not robot_selecionado:
                                print("Robot inválido ou não compatível.")
                                input("\nPressione ENTER para continuar...")
                                continue
                        # atribuir tarefa ao robot
                        if tarefa_objeto.atribuir_robot(id_robot):
                            db.atribuir_tarefa_bd(id_robot, id_tarefa)
                            print(f"Sucesso! Robot {id_robot} está a trabalhar na tarefa {id_tarefa}...")
                        else:
                            print("Falha ao atribuir tarefa. Verifique o estado da tarefa.")
                    else:
                        print("Tarefa inválida.")
                except ValueError:
                    print("ID inválido.")
            
            # Simulação -> imprementar depois

            # Confirmação (y/n)
            
            input("\nPressione ENTER para continuar...")

        elif opcao == '6':
            print("\n>> SIMULAÇÃO DO SISTEMA")
            print("1. Avançar 10 minutos (Manual)")
            print("2. Modo Automático (Contínuo)")
            
            escolha_sim = input("Escolha: ")
            
            if escolha_sim == '1':
                # MODO MANUAL (O que você já tinha)
                print("Processando...")
                logs = db.executar_simulacao_passo() # Chama a função que criamos antes
                if logs:
                    for msg in logs:
                        print(msg)
                else:
                    print("Não há robots a trabalhar")
                input("Pressione ENTER para continuar...")
                
            elif escolha_sim == '2':
                # MODO AUTOMÁTICO
                print("\n--- INICIANDO MODO AUTOMÁTICO ---")
                print("O sistema vai avançar 10 min a cada segundo.")
                print("Pressione CTRL+C para parar a simulação.\n")
                
                try:
                    ciclos = 0
                    while True:
                        ciclos += 1
                        logs = db.executar_simulacao_passo()
                        
                        # 2. Mostra o resultado
                        print(f"\n[Ciclo {ciclos} | +{ciclos*10} mins]")
                        if logs: 
                            for msg in logs:
                                print(msg)
                        else: # se não tiver mensagem para logo
                            print("Nenhum robot a trabalhar. Encerrando simulação...")
                            break
                        
                        # 3. Espera um pouco (ex: 1.5 segundos) antes do próximo
                        time.sleep(1.5) 
                        
                except KeyboardInterrupt:
                    # Isto captura quando você aperta Ctrl+C no terminal
                    print("\n\n>> Simulação interrompida pelo utilizador.")
                    input("Pressione ENTER para voltar ao menu...")

            elif opcao == '0':
                print("A encerrar sistema...")
                break

        elif opcao == '7':
            print("\n>> CONCLUIR / CANCELAR TAREFA")
            tarefas = db.listar_tarefas_bd()

            if not tarefas:
                print("Nenhuma tarefa encontrada.")
                input("Pressione ENTER para continuar...")
                continue

            for t in tarefas:
                print(t)

            try:
                id_tarefa = int(input("ID da tarefa a cancelar (0 para voltar): "))
            except ValueError:
                print("ID inválido.")
                input("Pressione ENTER para continuar...")
                continue

            if id_tarefa == 0:
                print("Operação cancelada.")
                input("Pressione ENTER para continuar...")
                continue

            db.cancelar_tarefa_bd(id_tarefa)
            input("Pressione ENTER para continuar...")
            
            
        elif opcao == '9':
            print("\n>> RELATÓRIO DE ALERTAS")

            # por enquanto, sem filtro de datas (pode adicionar depois)
            alertas = db.gerar_mapa_alertas()

            if not alertas:
                print("Nenhum alerta registado.")
                input("Pressione ENTER para continuar...")
                continue

            # Cabeçalho
            print("-" * 110)
            print(f"{'ID':<4} {'Robot':<6} {'Tipo':<20} {'Data/Hora':<25} Mensagem")
            print("-" * 110)

            for id_alerta, id_robot, tipo, data_hora, mensagem in alertas:
                data_base = str(data_hora).split(".")[0]   # tira milésimos
                data_sem_seg = data_base[:-3]              # tira os segundos -> "YYYY-MM-DD HH:MM"
                print(f"{id_alerta:<4} {str(id_robot):<6} {tipo:<20} {data_sem_seg:<25} {mensagem}")



            print("-" * 110)
            input("Pressione ENTER para continuar...")

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
