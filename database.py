# Arquivo: database.py
import sqlite3
from datetime import datetime

from models.robot import Robot 
from models.tarefa import Tarefa
import config


def inicializar_bd():
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
    
    try:    
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS robots (
                id_robot INTEGER PRIMARY KEY AUTOINCREMENT,
                modelo TEXT,
                estado TEXT,
                bateria INTEGER,
                deposito INTEGER,
                localizacao TEXT,
                tarefa_atual TEXT
            );
            CREATE TABLE IF NOT EXISTS tarefas (
                id_tarefa INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_limpeza TEXT,
                area TEXT,
                progresso REAL DEFAULT 0,
                estado TEXT,
                id_robot INTEGER,
                inicio DATETIME,
                fim DATETIME
            );
            CREATE TABLE IF NOT EXISTS historico_alertas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_robot INTEGER,
                tipo_alerta TEXT,  -- Ex: 'Bateria Fraca', 'Depósito Cheio', 'Avaria'
                data_hora DATETIME,
                mensagem TEXT,
                FOREIGN KEY(id_robot) REFERENCES robots(id_robot)
            );
            
        ''')
        conexao.commit()
        
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        if conexao:
            conexao.close()


# -------- ROBOTS -------- 

def adicionar_robot_bd(robot):
    """
    Recebe um objeto da classe Robot e salva no banco.
    """
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
    
    try:
        # [cite: 14] Funcionalidade de Adicionar
        cursor.execute("""
            INSERT INTO robots (modelo, estado, bateria, deposito, localizacao, tarefa_atual)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (robot.modelo, robot.estado, robot.bateria, 
            robot.deposito, robot.localizacao, robot.tarefa_atual))
        
        conexao.commit()
        print(f"Robot: {cursor.lastrowid} adicionado com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro ao adicionar tarefa: {e}")
        # Desfazer alterações em caso de erro
        try:
            conexao.rollback()
        except Exception:
            pass
        return False
    finally:
        if conexao:
            conexao.close()

def listar_robots_bd():
    """
    Busca os dados e converte de volta para objetos Robot.
    """
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
    
    try:
        cursor.execute("SELECT * FROM robots") # [cite: 21] Funcionalidade de Listar
        linhas = cursor.fetchall()
        
        lista_de_objetos = []
        for linha in linhas:
            # Reconstrói o objeto Robot a partir dos dados do banco
            novo_robot = Robot(*linha)
            lista_de_objetos.append(novo_robot)
            
        return lista_de_objetos
    except sqlite3.Error as e:
        print(f"Erro ao listar robots: {e}")
        return []
    finally:
        if conexao:
            conexao.close()
            
def remover_robot_db(id_robot):
    """"
    Remover robot da base de dados por parâmetro id
    """
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
        
    try:
        # verificar se existe robot com esse id
        cursor.execute("SELECT id_robot FROM robots WHERE id_robot = ?", (id_robot,))
        linha = cursor.fetchone()

        if linha is None:
            print("Não há robots com esse id")
            return False
        
        # existe, então remover
        cursor.execute("DELETE FROM robots WHERE id_robot = ?", (id_robot,))
        conexao.commit()
        
        print(f"Robot {id_robot} removido com sucesso!")
        return True
        
    except sqlite3.Error as e:
        print(f"Erro ao remover robot: {e}")
        return False
    finally:
        if conexao:
            conexao.close()


# -------- TAREFAS -------- 

def adicionar_tarefa_bd(tarefa):
    """
    Recebe um objeto da classe Tarefa e salva no banco.
    """
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO tarefas (tipo_limpeza, area, progresso, estado, id_robot, inicio, fim)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (tarefa.tipo_limpeza, tarefa.area, 0, tarefa.estado, 
                tarefa.id_robot, tarefa.inicio, tarefa.fim))

        # Garantir persistência da inserção
        conexao.commit()
        print(f"Tarefa: {cursor.lastrowid} adicionada com sucesso!")
        return True

    except sqlite3.Error as e:
        print(f"Erro ao adicionar tarefa: {e}")
        # Desfazer alterações em caso de erro
        try:
            conexao.rollback()
        except Exception:
            pass
        return False
    finally:
        if conexao:
            conexao.close()

def listar_tarefas_bd():
    """
    Busca os dados e converte de volta para objetos Tarefa.
    """
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
    
    try:
        cursor.execute("SELECT * FROM tarefas") 
        linhas = cursor.fetchall()
        
        lista_de_objetos = []
        for linha in linhas:
            # Reconstrói o objeto Tarefa a partir dos dados do banco
            # linha = (id_tarefa, tipo_limpeza, area, progresso, estado, id_robot, inicio, fim)
            nova_tarefa = Tarefa(linha[0], linha[1], linha[2], linha[4])
            nova_tarefa.id_robot = linha[5]
            nova_tarefa.inicio = linha[6]
            nova_tarefa.fim = linha[7]
            lista_de_objetos.append(nova_tarefa)
            
        return lista_de_objetos
    
    except sqlite3.Error as e:
        print(f"Erro ao listar tarefas: {e}")
        return []
    finally:
        if conexao:
            conexao.close()
            
def remover_tarefa_bd(id_tarefa):
    """
    Remove tarefa na base de dados por parametro id
    """
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
    
    try:
        cursor.execute("DELETE FROM tarefas WHERE id_tarefa = ?", (id_tarefa,))
        if cursor.rowcount > 0:
            print(f"Tarefa {id_tarefa} removida.")
            conexao.commit()
        else:
            print("Tarefa não encontrada.")
    except Exception as e:
        print("Erro:", e)
    finally:
        conexao.close()
            
            
# -------- OPERAÇÕES --------         

def atribuir_tarefa_bd(id_robot, id_tarefa):
    """
    Vincula um robot a uma tarefa pré-selecionados e atualiza os status de ambos.
    """
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
    
    try:
        # 1. Atualizar o ROBOT (Muda estado e define tarefa atual)
        cursor.execute("""
            UPDATE robots 
            SET estado = 'A Limpar', tarefa_atual = ?
            WHERE id_robot = ?
        """, (id_tarefa, id_robot))
        
        # 2. Atualizar a TAREFA (Muda estado, define robot e hora de inicio)
        hora_inicio = datetime.now()
        cursor.execute("""
            UPDATE tarefas
            SET estado = 'Em Progresso', id_robot = ?, inicio = ?
            WHERE id_tarefa = ?
        """, (id_robot, hora_inicio, id_tarefa))
        
        conexao.commit()
        print(f"Sucesso! Tarefa {id_tarefa} atribuída ao Robot {id_robot}.")
        return True
        
    except sqlite3.Error as e:
        print(f"Erro na atribuição: {e}")
        conexao.rollback() # Desfaz mudanças se algo der errado a meio
        return False
    finally:
        conexao.close()
        

def executar_simulacao_passo():
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
    mensagens = []
    
    try:
        cursor.execute("SELECT * FROM robots WHERE estado = 'A Limpar'")
        robots = cursor.fetchall()
        
        for robot in robots:
            # Desempacotar (ajuste índices se necessário)
            r_id, r_modelo, r_estado, r_bat, r_lixo, r_loc, r_tarefa_id = robot
            
            # Buscar dados da tarefa
            cursor.execute("SELECT tipo_limpeza, area, progresso FROM tarefas WHERE id_tarefa = ?", (r_tarefa_id,))
            dados_tarefa = cursor.fetchone()
            
            if dados_tarefa:
                tipo, nome_area, progresso_atual = dados_tarefa
                
                # 1. Pegar tamanho da área (se não existir, usa 20 como padrão)
                tamanho_area = config.AREAS_EMPRESA.get(nome_area, 20)
                
                # 2. Pegar perfil de consumo baseado no tipo (Aspiração/Lavagem)
                # Se o tipo não existir no config, usa valores padrão
                perfil = config.PERFIL_LIMPEZA.get(tipo, {
                    "consumo_bateria": 5, "encher_lixo": 5, "velocidade": 5
                })
                
                # 3. Aplicar os valores do config
                nova_bat = r_bat - perfil["consumo_bateria"]
                novo_lixo = r_lixo + perfil["encher_lixo"]
                
                avance_percentual = (perfil["velocidade"] / tamanho_area) * 100
                novo_progresso = progresso_atual + avance_percentual
                
                # Caso A: Bateria/Lixo Crítico - Problema
                if nova_bat <= config.LIMITE_BATERIA_CRITICO or novo_lixo >= config.LIMITE_DEPOSITO_CHEIO:
                    tipo_problema = ""
                    
                    if nova_bat <= config.LIMITE_BATERIA_CRITICO:
                        tipo_problema = "Bateria Fraca"
                    else:
                        tipo_problema = "Depósito Cheio"
                    
                    agora = datetime.now()
                    msg_erro = f"O robot parou a tarefa {r_tarefa_id} por {tipo_problema}."
                    
                    cursor.execute("""
                        INSERT INTO historico_alertas (id_robot, tipo_alerta, data_hora, mensagem)
                        VALUES (?, ?, ?, ?)
                    """, (r_id, tipo_problema, agora, msg_erro)) # para usar no relatório 

                    cursor.execute("UPDATE tarefas SET estado = 'Falhada', id_robot = NULL WHERE id_tarefa = ?", (r_tarefa_id,))
                    cursor.execute("UPDATE robots SET estado = ?, tarefa_atual = NULL WHERE id_robot = ?", (tipo_problema, r_id))
                    
                    mensagens.append(f"ALERTA GRAVADO: Robot {r_id} - {tipo_problema}")
                    pass 

                # Caso B: Terminou
                elif novo_progresso >= 100:
                    novo_estado_robot = "Estacionado"
                    agora = datetime.now()
                    
                    # Finaliza tarefa
                    cursor.execute("""
                        UPDATE tarefas 
                        SET estado = 'Concluida', progresso = 100, fim = ? 
                        WHERE id_tarefa = ?
                    """, (agora, r_tarefa_id))
                    
                    # Libera o robô (mantendo a bateria que sobrou)
                    cursor.execute("""
                        UPDATE robots 
                        SET estado = ?, bateria = ?, deposito = ?, tarefa_atual = NULL 
                        WHERE id_robot = ?
                    """, (novo_estado_robot, nova_bat, novo_lixo, r_id))
                    
                    mensagens.append(f"SUCESSO: Robot {r_id} concluiu a tarefa na {r_loc}! (Bat restante: {nova_bat}% | Depósito: {novo_lixo}%)")
                    pass

                # Caso C: Continua
                else:
                    # Atualiza robot
                    cursor.execute("UPDATE robots SET bateria = ?, deposito = ? WHERE id_robot = ?", (nova_bat, novo_lixo, r_id))
                    # Atualiza progresso da tarefa
                    cursor.execute("UPDATE tarefas SET progresso = ? WHERE id_tarefa = ?", (novo_progresso, r_tarefa_id))
                    mensagens.append(f"Robot {r_id} a trabalhar tarefa {r_tarefa_id} Progresso: {novo_progresso:.1f}% | Bat: {nova_bat}% | Lixo: {novo_lixo}%)")
                    pass
                    
        conexao.commit()
        return mensagens

    except Exception as e:
        return [f"Erro simulação: {e}"]
    finally:
        conexao.close()
    
    
# -------- RELATÓRIOS --------         
        
def gerar_mapa_alertas(data_inicio=None, data_fim=None):
    
    return 