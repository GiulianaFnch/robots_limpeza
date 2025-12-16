from datetime import datetime

class Tarefa:
    def __init__(self, id_tarefa, tipo_limpeza, area, estado = "Pendente"):
        self.id_tarefa = id_tarefa
        self.tipo_limpeza = tipo_limpeza
        self.area = area
        self.estado = estado
        self.id_robot = None
        self.inicio = None
        self.fim = None

    def __str__(self):
        return f"[Tarefa {self.id_tarefa}] - Tipo de limpeza: {self.tipo_limpeza} - Área/Divisão: {self.area} - Estado: {self.estado} - ID Robot: {self.id_robot} | Início: {self.inicio} - Fim: {self.fim}"
    
    def iniciar_tarefa(self, id_robot):
        if self.estado != "Pendente":
            print("A tarefa só pode ser iniciada se estiver pendente.")
            return False
        self.estado = "Em Progresso"
        self.id_robot = id_robot
        self.inicio = datetime.now()
        return True
    
    def concluir_tarefa(self):
        if self.estado != "Em Progresso":
            print("A tarefa só pode ser concluída se estiver em progresso.")
            return False
        self.estado = "Concluída"
        self.fim = datetime.now()
        return True
    
    def atribuir_robot(self, id_robot):
        if self.estado != "Pendente":
            print("A tarefa só pode ser atribuída se estiver pendente.")
            return False
        self.id_robot = id_robot
        return True