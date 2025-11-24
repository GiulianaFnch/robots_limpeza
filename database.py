# Arquivo: database.py
import sqlite3
from models.robot import Robot 

def adicionar_robot_bd(robot):
    """
    Recebe um objeto da classe Robot e salva no banco.
    """
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
    
    # [cite: 14] Funcionalidade de Adicionar
    cursor.execute("""
        INSERT INTO robots (id, modelo, estado, bateria, deposito, localizacao)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (robot.id, robot.modelo, robot.estado, robot.nivel_bateria, 
          robot.capacidade_deposito, robot.localizacao))
    
    conexao.commit()
    conexao.close()

def listar_robots_bd():
    """
    Busca os dados e converte de volta para objetos Robot.
    """
    # ... código de conexão ...
    cursor.execute("SELECT * FROM robots") # [cite: 21] Funcionalidade de Listar
    linhas = cursor.fetchall()
    
    lista_de_objetos = []
    for linha in linhas:
        # Reconstrói o objeto Robot a partir dos dados do banco
        novo_robot = Robot(linha[0], linha[1], linha[5]) 
        # (Você precisaria ajustar o construtor ou setar os atributos manualmente aqui)
        novo_robot.estado = linha[2]
        novo_robot.nivel_bateria = linha[3]
        lista_de_objetos.append(novo_robot)
        
    return lista_de_objetos