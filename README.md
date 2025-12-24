# Sistema de Gestão de Robots de Limpeza 

Este projeto é uma aplicação em **Python** desenvolvida no âmbito da cadeira de **Fundamentos de Programação no ISLA Gaia**. O sistema permite gerir uma frota de robots de limpeza, atribuir tarefas em diferentes áreas de uma empresa e simular a execução dessas limpezas com um ciclo de vida autónomo (trabalho, carregamento e avarias).

![Print screen do menu principal do projeto](/assets/images/print.png)

## Funcionalidades Principais

### 1. Gestão de Frota
  * **Adicionar Robots:** Criação de novos robots definindo o modelo (Aspirador, Lavador ou Híbrido) e a localização inicial.
  * **Listagem em Tempo Real:** Visualização do estado atual (Bateria, Depósito, Localização e Estado: *Estacionado, A Limpar, A Carregar, Com Avaria*).
  * **Manutenção:** Remoção de robots obsoletos ou avariados.

### 2. Gestão de Tarefas
  * **Criação de Tarefas:** Agendamento de limpezas (Aspiração ou Lavagem) para áreas específicas (ex: Receção, Cozinha).
  * **Atribuição Inteligente:** O sistema verifica compatibilidade antes de iniciar:
      * O robot tem o modelo correto?
      * O robot está na localização correta?
      * O robot está operacional (sem avarias)?
  * **Cancelamento:** Possibilidade de cancelar tarefas em curso e libertar os robots.

### 3. Simulação e Ciclo de Vida
  * **Simulação de Tempo:** Avanço manual ou automático do tempo, calculando o progresso da limpeza, consumo de bateria e enchimento do depósito.
  * **Recuperação Automática:** Robots com bateria fraca (<20%) ou depósito cheio regressam automaticamente à base (`A Carregar`), recuperam os recursos e voltam ao estado `Estacionado` quando prontos.
  * **Sistema de Desgaste:** Se um robot acumular demasiados alertas no histórico (configurável), entra em estado de `Com Avaria` e deixa de operar permanentemente.

### 4. Relatórios e Estatísticas (Business Intelligence)
  * **Mapa de Horas:** Cálculo das horas de trabalho simuladas por cada robot (filtrado por datas ou histórico total).
  * **Hotspots (Áreas Frequentes):** Ranking das divisões que mais vezes foram limpas.
  * **Análise de Eficiência:** Comparativo de tempo médio gasto por cada modelo de robot e por cada área da empresa.
  * **Histórico de Alertas:** Log detalhado de todas as ocorrências (bateria fraca, depósito cheio, avarias).

---

## Como Executar

### Pré-requisitos
  * Python 3.x instalado.
  * Bibliotecas padrão utilizadas: `sqlite3`, `datetime`, `time`, `sys`.

### Passo a Passo
1.  Clone este repositório ou descarregue os ficheiros.
2.  Abra o terminal na pasta do projeto.
3.  Execute o ficheiro principal:

```bash
python main.py
```
Nota: A base de dados gestao_robots.db será criada automaticamente na primeira execução.

## Estrutura do Projeto

  * `main.py`: O "cérebro" da aplicação. Contém o menu interativo (CLI) e a orquestração das funcionalidades.
  * `database.py`: Camada de persistência e lógica de negócio. Gere a conexão SQLite, executa a simulação de tempo, gere as avarias automáticas e calcula os relatórios estatísticos.
  * `config.py`: Ficheiro de configurações globais. Define:
      * Tamanho das áreas (m²).
      * Consumo e velocidade dos robots.
      * **Taxas de carregamento e limites de tolerância a avarias.**
  * `models/`: Classes que representam as entidades.
      * `robot.py`: Definição e validação do robot.
      * `tarefa.py`: Definição e estados da tarefa.
  * `gestao_robots.db`: Ficheiro da base de dados (gerado automaticamente na primeira execução).

-----

## Configuração Personalizada

Pode ajustar a "física" da simulação e as regras de negócio editando o ficheiro `config.py`. Para além das áreas, agora pode configurar a recuperação e o desgaste dos robots:

```python
# --- RECUPERAÇÃO ---
# Velocidade de recuperação na base (por passo de simulação)
TAXA_CARREGAMENTO = 15      # Ganha 15% de bateria
TAXA_ESVAZIAMENTO = 50      # Esvazia 50% do depósito

# --- TOLERÂNCIA A FALHAS ---
# Se o robot atingir este número total de alertas no histórico, ele avaria permanentemente.
LIMITE_ALERTAS_PARA_AVARIA = 5
```
## Tecnologias Utilizadas
Linguagem: Python 3

Base de Dados: SQLite3

Paradigma: Programação Orientada a Objetos (POO) e Estruturada.

## Autores
Projeto desenvolvido por Giuliana Finochio e Pedro Costa para o ISLA Gaia.
