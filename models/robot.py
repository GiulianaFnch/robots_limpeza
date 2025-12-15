#criando a classe 
import config


class Robot:
    def __init__(self, id_robot, modelo, estado = "Estacionado",bateria = 100, deposito = 0, localizacao = "Base", tarefa_atual = None ):
        self.id_robot = id_robot       #Identificador único.
        self.modelo = modelo        #Modelo (aspirador, lavador, hibrido).
        self.estado = estado        #Estado (estacionado, com avaria, etc...).
        self.bateria = bateria      #Nivel de bateria(%).
        self.deposito = deposito        #Deposito de lixo (%).
        self.localizacao = localizacao      #Localizaçõ do robot.
        self.tarefa_atual = tarefa_atual        #Tarefa atribuida no momento.

    def __str__(self):      
        #Representação em texto do robot (util para o print).

        return f"[Robot {self.id_robot}] {self.modelo} - Bat: {self.bateria}% | Lixo: {self.deposito}% - Estado: {self.estado}"
    
    def pode_trabalhar(self):       
        # Verifica se o robot tem bateria e espaço no depósito usando limites do config.

        # Bateria acima do limite crítico definido no config
        bateria_ok = self.bateria > config.LIMITE_BATERIA_CRITICO

        # Depósito abaixo do limite cheio definido no config
        deposito_ok = self.deposito < config.LIMITE_DEPOSITO_CHEIO

        avaria = self.estado == "Com Avaria"
        return bateria_ok and deposito_ok and not avaria
    
    def consumir_recursos(self, gasto_bateria, enchimento_deposito):
        #simula o consumo do robot até o final de uma tarefa.

        self.nivel_bateria -= gasto_bateria
        self.nivel_deposito += enchimento_deposito

        #Validações de limites (não deixa a bateria abaixo de 0% ou o depósito acima de 100%)
        if self.nivel_bateria < 0: self.nivel_bateria = 0
        if self.nivel_deposito > 100: self.nivel_deposito = 100
