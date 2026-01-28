class Pedido:
    def __init__(self):
        self.itens = []

    # TODO: Crie um método chamado adicionar_item que recebe um preço e adiciona à lista de itens:
    def adicionar_itens(self, nome, preco):
        # TODO: Adicione o preço do item à lista:
        self.itens.append((nome, preco))

    # TODO: Crie um método chamado calcular_total que retorna a soma de todos os preços da lista:
    def total_pedido(self):
        total = 0.0
        # TODO: Retorne a soma de todos os preços
        for preco in self.itens:
            total += float(preco[1])
        return total


quantidade_pedidos = int(input().strip())

pedido = Pedido()

for _ in range(quantidade_pedidos):
    entrada = input().strip()
    nome, preco = entrada.rsplit(" ", 1)
    # TODO: Chame o método adicionar_item corretamente:
    pedido.adicionar_itens(nome=nome, preco=preco)

# TODO: Exiba o total formatado com duas casas decimais:
print(f"{pedido.total_pedido():.2f}")
