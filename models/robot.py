#criando a classe 
class Robot:
    def __init__(self, id_robot, modelo, estado = "Estacionado",bateria = 100, deposito = 0, localizacao = "Base", tarefa_atual = None ):
        self.id_robot = id_robot       #Identificador único.
        self.modelo = modelo        #Modelo (aspirador, lavador, hibrido).
        self.estado = estado        #Estado (estacionado, com avaria, etc...).
        self.bateria = bateria      #Nivel de bateria(%).
        self.deposito = deposito        #Deposito de lixo (%).
        self.localizacao = localizacao      #Localizaçõ do robot.
        self.tarefa_atual = tarefa_atual        #Tarefa atribuida no momento