# Sistema de Gestão de Robots de Limpeza 

Este projeto é uma aplicação em **Python** desenvolvida no âmbito da cadeira de **Fundamentos de Programação no ISLA Gaia**. O sistema permite gerir uma frota de robots de limpeza, atribuir tarefas em diferentes áreas de uma empresa e simular a execução dessas limpezas com gestão de recursos (bateria e depósito).

## Funcionalidades Principais

### 1\. Gestão de Frota

  * **Adicionar Robots:** Criação de novos robots definindo o modelo (Aspirador, Lavador ou Híbrido) e a localização inicial.
  * **Listagem:** Visualização do estado atual de todos os robots (Bateria, Depósito, Localização e Estado).
  * **Remoção:** Exclusão de robots do sistema.

### 2\. Gestão de Tarefas

  * **Criação de Tarefas:** Agendamento de limpezas (Aspiração ou Lavagem) para áreas específicas (ex: Receção, Cozinha).
  * **Atribuição Inteligente:** O sistema verifica compatibilidade antes de atribuir uma tarefa:
      * O robot tem o modelo correto para a tarefa?
      * O robot está na localização correta?
      * O robot tem bateria suficiente e depósito vazio?

### 3\. Simulação do Sistema

  * **Passo-a-Passo ou Automático:** O sistema simula o passar do tempo, calculando:
      * O progresso da limpeza com base na velocidade do robot e tamanho da área.
      * O consumo de bateria.
      * O enchimento do depósito de lixo.
  * **Alertas Automáticos:** Interrupção automática e registo de alerta se a bateria ficar crítica (\<20%) ou o depósito encher (100%).

### 4\. Relatórios e Persistência

  * **Base de Dados SQLite:** Todos os dados (robots, tarefas, histórico) são guardados automaticamente no ficheiro `gestao_robots.db`.
  * **Histórico de Alertas:** Consulta de falhas ocorridas durante as simulações.

-----

## Como Executar

### Pré-requisitos

  * Python 3.x instalado.
  * Não são necessárias bibliotecas externas (utiliza apenas bibliotecas padrão: `sqlite3`, `datetime`, `time`, `sys`).

### Passo a Passo

1.  Clone este repositório ou descarregue os ficheiros.
2.  Abra o terminal na pasta do projeto.
3.  Execute o ficheiro principal:

<!-- end list -->

```bash
python main.py
```

-----

## Estrutura do Projeto

  * `main.py`: O ponto de entrada da aplicação. Contém o menu interativo (CLI) e a lógica de interação com o utilizador.
  * `database.py`: Gere a conexão com o banco de dados SQLite, criando tabelas e executando queries (CRUD).
  * `config.py`: Ficheiro de configurações globais. Define:
      * Tamanho das áreas (m²).
      * Consumo de bateria e velocidade por tipo de limpeza.
      * Limites críticos de bateria e lixo.
  * `models/`: Contém as classes que representam as entidades do sistema.
      * `robot.py`: Lógica do robot (consumo de recursos, validação de estado).
      * `tarefa.py`: Lógica da tarefa (estados, tempos de início/fim).
  * `gestao_robots.db`: Ficheiro da base de dados (gerado automaticamente na primeira execução).

-----

## Configuração

Pode ajustar os parâmetros da simulação editando o ficheiro `config.py`. Exemplo de configurações personalizáveis:

```python
# Mapeamento: Nome da Área -> Tamanho em m²
AREAS_EMPRESA = {
    "Receção": 50,
    "Salão": 100
}

# Definição de limites
LIMITE_BATERIA_CRITICO = 20
```

-----

## Tecnologias Utilizadas

  * **Linguagem:** Python 3
  * **Base de Dados:** SQLite3
  * **Paradigma:** Programação Orientada a Objetos (POO)

-----

## Autores

Projeto desenvolvido por **Giuliana Finochio** e **Pedro Costa** para o ISLA Gaia.