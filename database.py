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
        
        
def cancelar_tarefa_bd(id_tarefa):
    """
    Cancela uma tarefa e liberta o robot associado (se existir).
    """
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()

    try:
        # buscar tarefa
        cursor.execute("""
            SELECT id_robot, estado
            FROM tarefas
            WHERE id_tarefa = ?
        """, (id_tarefa,))
        linha = cursor.fetchone()

        if linha is None:
            print("Tarefa não encontrada.")
            return False

        id_robot, estado_atual = linha

        # só faz sentido cancelar se não estiver já concluída/falhada/cancelada
        if estado_atual in ("Concluida", "Falhada", "Cancelada"):
            print(f"Não é possível cancelar uma tarefa com estado '{estado_atual}'.")
            return False

        # 1) atualizar tarefa -> Cancelada
        cursor.execute("""
            UPDATE tarefas
            SET estado = 'Cancelada'
            WHERE id_tarefa = ?
        """, (id_tarefa,))

        # 2) se tiver robot ligado, libertar robot
        if id_robot is not None:
            cursor.execute("""
                UPDATE robots
                SET estado = 'Estacionado', tarefa_atual = NULL
                WHERE id_robot = ?
            """, (id_robot,))

        conexao.commit()
        print(f"Tarefa {id_tarefa} cancelada com sucesso.")
        return True

    except sqlite3.Error as e:
        print(f"Erro ao cancelar tarefa: {e}")
        conexao.rollback()
        return False
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
        # PARTE 1: ROBOTS A TRABALHAR (Consomem Bateria / Enchem Lixo)
        
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
                
                # --- Lógica de Consumo ---
                tamanho_area = config.AREAS_EMPRESA.get(nome_area, 20)
                perfil = config.PERFIL_LIMPEZA.get(tipo, {"consumo_bateria": 5, "encher_lixo": 5, "velocidade": 5})
                
                nova_bat = r_bat - perfil["consumo_bateria"]
                novo_lixo = r_lixo + perfil["encher_lixo"]
                avance_percentual = (perfil["velocidade"] / tamanho_area) * 100
                novo_progresso = progresso_atual + avance_percentual
                
                # Caso A: Bateria/Lixo Crítico -> VAI PARA A BASE
                if nova_bat <= config.LIMITE_BATERIA_CRITICO or novo_lixo >= config.LIMITE_DEPOSITO_CHEIO:
                    
                    tipo_problema = "Bateria Fraca" if nova_bat <= config.LIMITE_BATERIA_CRITICO else "Depósito Cheio"
                    agora = datetime.now()
                    msg_erro = f"O robot parou a tarefa {r_tarefa_id} por {tipo_problema}."
                    
                    # 1. Regista o Alerta
                    cursor.execute("""
                        INSERT INTO historico_alertas (id_robot, tipo_alerta, data_hora, mensagem)
                        VALUES (?, ?, ?, ?)
                    """, (r_id, tipo_problema, agora, msg_erro))
                    
                    # 2. VERIFICAÇÃO DE AVARIA 
                    # Conta quantos alertas este robot já teve na vida
                    cursor.execute("SELECT COUNT(*) FROM historico_alertas WHERE id_robot = ?", (r_id,))
                    total_alertas = cursor.fetchone()[0]
                    
                    novo_estado = 'A Carregar' # O padrão é ir carregar
                    msg_extra = "Iniciando recarga..."
                    
                    # Se ultrapassou o limite, muda para 'Com Avaria'
                    if total_alertas >= config.LIMITE_ALERTAS_PARA_AVARIA:
                        novo_estado = 'Com Avaria'
                        msg_extra = "CRÍTICO: Limite de alertas excedido. Robot avariou e precisa de técnico!"
                    
                        cursor.execute("""
                            INSERT INTO historico_alertas (id_robot, tipo_alerta, data_hora, mensagem)
                            VALUES (?, ?, ?, ?)
                        """, (r_id, "AVARIA TOTAL", agora, "O robot avariou por excesso de desgaste."))

                    # 3. Atualiza o Robot (ou vai carregar, ou avaria de vez)
                    cursor.execute("UPDATE tarefas SET estado = 'Falhada', id_robot = NULL WHERE id_tarefa = ?", (r_tarefa_id,))
                    cursor.execute("UPDATE robots SET estado = ?, tarefa_atual = NULL WHERE id_robot = ?", (novo_estado, r_id))
                    
                    mensagens.append(f"ALERTA: Robot {r_id} parou ({tipo_problema}). {msg_extra}")
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
                
        # PARTE 2: ROBOTS NA BASE (Recuperam Bateria / Esvaziam Lixo)
        
        cursor.execute("SELECT * FROM robots WHERE estado = 'A Carregar'")
        robots_carregando = cursor.fetchall()
        
        for robot in robots_carregando:
            r_id, r_modelo, r_estado, r_bat, r_lixo, r_loc, r_tarefa_id = robot
            
            nova_bat = r_bat + config.TAXA_CARREGAMENTO
            novo_lixo = r_lixo - config.TAXA_ESVAZIAMENTO
            
            # Limites (Não passar de 100 nem ser menor que 0)
            if nova_bat > 100: nova_bat = 100
            if novo_lixo < 0: novo_lixo = 0
            
            # Se já está 100% pronto, volta a estar disponivel ('Estacionado')
            if nova_bat == 100 and novo_lixo == 0:
                cursor.execute("UPDATE robots SET estado = 'Estacionado', bateria = ?, deposito = ? WHERE id_robot = ?", (nova_bat, novo_lixo, r_id))
                mensagens.append(f"MANUTENÇÃO: Robot {r_id} está 100% carregado e pronto a usar!")
            else:
                # Continua a carregar
                cursor.execute("UPDATE robots SET bateria = ?, deposito = ? WHERE id_robot = ?", (nova_bat, novo_lixo, r_id))
                mensagens.append(f"Robot {r_id} na base a carregar... (Bat: {nova_bat}% | Lixo: {novo_lixo}%)")

        conexao.commit()
            
        return mensagens

    except Exception as e:
        return [f"Erro simulação: {e}"]
    finally:
        conexao.close()
    
    
# -------- RELATÓRIOS --------         
        
def gerar_mapa_alertas(data_inicio=None, data_fim=None):
    """
    Devolve uma lista de alertas (id, id_robot, tipo, data_hora, mensagem),
    opcionalmente filtrada por intervalo de datas.
    """
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()

    try:
        sql_base = """
            SELECT id, id_robot, tipo_alerta, data_hora, mensagem
            FROM historico_alertas
        """
        if data_inicio and data_fim:
            sql_base += " WHERE data_hora BETWEEN ? AND ?"
            params = (data_inicio, data_fim)
        else:
            params = ()
            
        # 1. Agrupa visualmente por Robot (id_robot ASC)
        # 2. Dentro de cada robot, mostra o mais recente primeiro (data_hora DESC)
        sql_base += " ORDER BY id_robot ASC, data_hora DESC"

        cursor.execute(sql_base, params)
        return cursor.fetchall()
        
    except sqlite3.Error as e:
        print(f"Erro ao gerar mapa de alertas: {e}")
        return []
    finally:
        conexao.close()

def gerar_mapa_areas_frequentes():
    """
    Retorna uma lista de áreas ordenadas pela frequência de limpeza.
    Output: [('Receção', 5), ('Cozinha', 2), ...]
    """
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
    
    try:
        # Agrupa por área e conta quantas tarefas CONCLUÍDAS existem em cada uma
        cursor.execute("""
            SELECT area, COUNT(*) as qtd
            FROM tarefas
            WHERE estado = 'Concluida'
            GROUP BY area
            ORDER BY qtd DESC
        """)
        return cursor.fetchall()
        
    except sqlite3.Error as e:
        print(f"Erro no mapa de áreas: {e}")
        return []
    finally:
        conexao.close()


def gerar_estatisticas_eficiencia():
    """
    Retorna dois conjuntos de dados:
    1. Eficiência por Modelo (Tempo médio por tipo de robot)
    2. Eficiência por Área (Tempo médio por divisão)
    """
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
    
    dados_modelo = []
    dados_area = []
    
    try:
        # 1. Média por MODELO DE ROBOT
        cursor.execute("""
            SELECT 
                r.modelo, 
                COUNT(*) as qtd_tarefas,
                AVG((julianday(t.fim) - julianday(t.inicio)) * 1440) as media_minutos
            FROM robots r
            JOIN tarefas t ON r.id_robot = t.id_robot
            WHERE t.estado = 'Concluida'
            GROUP BY r.modelo
            ORDER BY media_minutos ASC
        """)
        dados_modelo = cursor.fetchall()

        # 2. Média por ÁREA
        cursor.execute("""
            SELECT 
                t.area, 
                COUNT(*) as qtd_tarefas,
                AVG((julianday(t.fim) - julianday(t.inicio)) * 1440) as media_minutos
            FROM tarefas t
            WHERE t.estado = 'Concluida'
            GROUP BY t.area
            ORDER BY media_minutos DESC
        """)
        dados_area = cursor.fetchall()
        
        return dados_modelo, dados_area

    except sqlite3.Error as e:
        print(f"Erro estatísticas: {e}")
        return [], []
    finally:
        conexao.close()


def gerar_mapa_horas_trabalho(data_inicio=None, data_fim=None):
    """
    Calcula horas SIMULADAS baseadas no tamanho da área e velocidade do robot.
    Retorna lista: [(id_robot, modelo, total_horas_simuladas, qtd_tarefas), ...]
    """
    conexao = sqlite3.connect('gestao_robots.db')
    cursor = conexao.cursor()
    
    try:
        # 1. Buscamos os dados BRUTOS das tarefas concluídas
        # Não somamos nada no SQL, trazemos tudo para calcular no Python
        query = """
            SELECT r.id_robot, r.modelo, t.tipo_limpeza, t.area
            FROM robots r
            JOIN tarefas t ON r.id_robot = t.id_robot
            WHERE t.estado = 'Concluida'
        """
        
        params = []
        if data_inicio and data_fim:
            query += " AND t.inicio >= ? AND t.inicio <= ?"
            params.append(f"{data_inicio} 00:00:00")
            params.append(f"{data_fim} 23:59:59")
            
        cursor.execute(query, params)
        linhas = cursor.fetchall()
        
        # 2. Processamento Matemático (Agrupamento Manual)
        # Estrutura: { id_robot: {'modelo': 'X', 'horas': 0.0, 'qtd': 0} }
        relatorio = {}
        
        for linha in linhas:
            r_id, r_modelo, t_tipo, t_area = linha
            
            # --- O CÁLCULO DE TEMPO SIMULADO ---
            # A. Tamanho da Área (m²)
            tamanho = config.AREAS_EMPRESA.get(t_area, 20) # 20 é padrão se não achar
            
            # B. Velocidade (m² por passo)
            perfil = config.PERFIL_LIMPEZA.get(t_tipo, {"velocidade": 5})
            velocidade = perfil["velocidade"]
            
            # C. Quantos passos (de 10 min) demorou?
            passos = tamanho / velocidade
            
            # D. Total em Horas (Passos * 10 min / 60 min)
            horas_tarefa = (passos * 10) / 60
            # -----------------------------------
            
            # Adicionar ao dicionário acumulador
            if r_id not in relatorio:
                relatorio[r_id] = {'modelo': r_modelo, 'horas': 0.0, 'qtd': 0}
            
            relatorio[r_id]['horas'] += horas_tarefa
            relatorio[r_id]['qtd'] += 1
            
        # 3. Converter dicionário para lista ordenada (para o main.py ler igual antes)
        # Formato final: (id, modelo, horas, qtd)
        resultados_finais = []
        for r_id, dados in relatorio.items():
            resultados_finais.append((
                r_id, 
                dados['modelo'], 
                dados['horas'], 
                dados['qtd']
            ))
            
        # Ordenar quem trabalhou mais (horas descrescente)
        resultados_finais.sort(key=lambda x: x[2], reverse=True)
        
        return resultados_finais
        
    except sqlite3.Error as e:
        print(f"Erro ao calcular horas simuladas: {e}")
        return []
    finally:
        conexao.close()