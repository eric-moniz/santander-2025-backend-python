# Dicionário para agrupar participantes por tema
eventos = {}

# Entrada do número de participantes
n = int(input().strip())

# TODO: Crie um loop para armazenar participantes e seus temas:
for _ in range(n):
    entrada = input()

    participante, tema = entrada.split(", ")

    if tema in eventos.keys():
        eventos[tema].append(participante)
    else:
        eventos.update({tema: [participante]})

# Exibe os grupos organizados
for tema, participantes in eventos.items():
    print(f"{tema}: {', '.join(participantes)}")

"""
-- TESTE --
Entrada:
5
Ana, Tecnologia
Carlos, Esportes
Maria, Tecnologia
Pedro, Música
João, Esportes

Saida:
Tecnologia: Ana, Maria
Esportes: Carlos, João
Música: Pedro
"""
