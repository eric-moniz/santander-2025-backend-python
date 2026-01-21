# Lista para armazenar os produtos e preços
carrinho = []
total = 0.0

# Entrada do número de itens
n = int(input().strip())

# Loop para adicionar itens ao carrinho
for _ in range(n):
    linha = input().strip()

    # Encontra a última ocorrência de espaço para separar nome e preço
    posicao_espaco = linha.rfind(" ")

    # Separa o nome do produto e o preço
    item = linha[:posicao_espaco]
    preco = float(linha[posicao_espaco + 1 :])

    # Adiciona ao carrinho
    carrinho.append((item, preco))
    total += preco

# TODO: Exiba os itens e o total da compra
for item, preco in carrinho:
    print(f"{item}: R${preco:.2f}")

print(f"Total: R${total:.2f}")

"""
--- TESTES ---
Entrada
2
Pão 3.50
Leite 4.00

Saida:
Pão: R$3.50
Leite: R$4.00
Total: R$7.50

Entrada
3
Arroz 2.50
Brigadeiro 3.00
Sorvete 14.50

Saida:
Arroz: R$2.50
Brigadeiro: R$3.00
Sorvete: R$14.50
Total: R$20.00

Entrada:
3
Maçã 2.00
Pera 3.50
Biscoito 5.50

Saida:
Maçã: R$2.00
Pera: R$3.50
Biscoito: R$5.50
Total: R$11.00
"""
