# Entrada do número de pacientes
n = int(input().strip())

# Lista para armazenar pacientes
pacientes = []

# Lista para ordem de atendimento
ordem_atendimento = []
# Loop para entrada de dados
for _ in range(n):
    nome, idade, status = input().strip().split(", ")
    idade = int(idade)
    pacientes.append((nome, idade, status))

# TODO: Ordene por prioridade: urgente > idosos > demais:
# Ordenação customizada:
# 1. Status: 'urgente' vira 0, 'normal' vira 1 (0 vem antes de 1)
# 2. Idade: Usamos -x[1] para que a maior idade venha primeiro
# 3. Demais: Idade (x[1]) como critério de desempate
prioridade = sorted(
    pacientes, key=lambda x: (0 if x[2] == "urgente" else 1, -x[1], x[1])
)

# TODO: Exiba a ordem de atendimento com título e vírgulas:
for nome in prioridade:
    ordem_atendimento.append(nome[0])
print(f"Ordem de Atendimento: {', '.join(ordem_atendimento)}")

# TESTES
"""
Entrada:
4
Paula, 30, normal
Ricardo, 60, normal
Tiago, 60, urgente
Amanda, 50, urgente
Saida:
Ordem de Atendimento: Tiago, Amanda, Ricardo, Paula
=====================================================
Entrada:
5
João, 65, normal
Maria, 80, urgente
Lucas, 50, normal
Fernanda, 25, normal
Pedro, 90, urgente

Saída:
Ordem de Atendimento: Pedro, Maria, João, Lucas, Fernanda
"""
