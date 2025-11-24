class Tarefa:
    def __init__(self, id_tarefa, tipo_limpeza, area, estado = "Pendente"):
        self.id_tarefa = id_tarefa
        self.tipo_limpeza = tipo_limpeza
        self.area = area
        self.estado = estado
        self.id_robot = None
        self.inicio = None
        self.fim = None