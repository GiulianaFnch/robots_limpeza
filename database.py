# Arquivo: database.py
import sqlite3
from models.robot import Robot 

def criar_banco():
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS robots (
            id_robot INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT,
            estado TEXT,
            bateria INTEGER,
            deposito INTEGER,
            localizacao TEXT,
            tarefa_atual TEXT
        )
    ''')
    conexao.commit()
    conexao.close()

def adicionar_robot_bd(robot):
    criar_banco()
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
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM robots") # [cite: 21] Funcionalidade de Listar
    linhas = cursor.fetchall()
    conexao.close()
    
    lista_de_objetos = []
    for linha in linhas:
        # Reconstrói o objeto Robot a partir dos dados do banco
        # A ordem das colunas no banco deve corresponder à ordem dos argumentos no construtor
        novo_robot = Robot(*linha)
        lista_de_objetos.append(novo_robot)
        
    return lista_de_objetos