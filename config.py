# --- DEFINIÇÃO DA EMPRESA ---
# Mapeamento: Nome da Área -> Tamanho em m²
AREAS_EMPRESA = {
    "Receção": 50,
    "Escritório A": 30,
    "Escritório B": 30,
    "Cozinha": 20,
    "Corredor": 15,
    "Salão": 100
}

# --- PARÂMETROS DE CONSUMO E VELOCIDADE ---
# Aqui definimos quanto cada tipo de tarefa gasta por "passo" (ex: 10 min)
PERFIL_LIMPEZA = {
    "Lavagem": {
        "consumo_bateria": 8,   # %
        "encher_lixo": 5,       # %
        "velocidade": 5         # m² por passo
    },
    "Aspiração": {
        "consumo_bateria": 3,   # %
        "encher_lixo": 10,      # %
        "velocidade": 10        # m² por passo
    }
}

# --- LIMITES DO SISTEMA ---
LIMITE_BATERIA_CRITICO = 20
LIMITE_DEPOSITO_CHEIO = 100