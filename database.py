# Arquivo: database.py
import sqlite3
from datetime import datetime
from models.robot import Robot 
from models.tarefa import Tarefa


def inicializar_bd():
    try:    
        conexao = sqlite3.connect('gestao_robots.db')
        cursor = conexao.cursor()
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
                estado TEXT,
                id_robot INTEGER,
                inicio DATETIME,
                fim DATETIME
            );
            
        ''')
        conexao.commit()
        
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        if conexao:
            conexao.close()




def adicionar_robot_bd(robot):
    """
    Recebe um objeto da classe Robot e salva no banco.
    """
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
    
    # [cite: 14] Funcionalidade de Adicionar
    cursor.execute("""
        INSERT INTO robots (modelo, estado, bateria, deposito, localizacao, tarefa_atual)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (robot.modelo, robot.estado, robot.bateria, 
          robot.deposito, robot.localizacao, robot.tarefa_atual))
    
    print(f"Robot: {cursor.lastrowid} adicionado com sucesso!")

    conexao.commit()
    conexao.close()

def listar_robots_bd():
    """
    Busca os dados e converte de volta para objetos Robot.
    """
    try:
        conexao = sqlite3.connect('gestao_robots.db')
        cursor = conexao.cursor()
        
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
    try:
        conexao = sqlite3.connect('gestao_robots.db')
        cursor = conexao.cursor()
        
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
    
    cursor.execute("""
        INSERT INTO tarefas (tipo_limpeza, area, estado, id_robot, inicio, fim)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (tarefa.tipo_limpeza, tarefa.area, tarefa.estado, 
          tarefa.id_robot, tarefa.inicio, tarefa.fim))
    
    print(f"Robot: {cursor.lastrowid} adicionado com sucesso!")

    conexao.commit()
    conexao.close()

def listar_tarefas_bd():
    """
    Busca os dados e converte de volta para objetos Tarefa.
    """
    try:
        conexao = sqlite3.connect('gestao_robots.db')
        cursor = conexao.cursor()
        
        cursor.execute("SELECT * FROM tarefas") 
        linhas = cursor.fetchall()
        
        lista_de_objetos = []
        for linha in linhas:
            # Reconstrói o objeto Tarefa a partir dos dados do banco
            # linha = (id_tarefa, tipo_limpeza, area, estado, id_robot, inicio, fim)
            nova_tarefa = Tarefa(linha[0], linha[1], linha[2], linha[3])
            nova_tarefa.id_robot = linha[4]
            nova_tarefa.inicio = linha[5]
            nova_tarefa.fim = linha[6]
            lista_de_objetos.append(nova_tarefa)
            
        return lista_de_objetos
    
    except sqlite3.Error as e:
        print(f"Erro ao listar tarefas: {e}")
        return []
    finally:
        if conexao:
            conexao.close()
            
            

def atribuir_tarefa_robot(id_robot, id_tarefa):
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