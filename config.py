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
# Quanto cada tipo de tarefa gasta por passo (10 min)
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

# --- RECUPERAÇÃO ---
# Quanto recupera por cada passo de simulação 
TAXA_CARREGAMENTO = 15      # Ganha 15% de bateria
TAXA_ESVAZIAMENTO = 50      # Esvazia 50% do depósito

# --- AVARIAS E MANUTENÇÃO ---
# Se o robot atingir este número total de alertas no histórico, ele avaria.
LIMITE_ALERTAS_PARA_AVARIA = 5  # Ex: Ao 5º erro, o robot quebra.