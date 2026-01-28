# Definindo a superclasse
class Veiculo:
    def __init__(self, _tipo, modelo, km):
        self._tipo = _tipo
        self.modelo = modelo
        self.km = km


# Definindo a subclasse que herda de Veiculo
class Carro(Veiculo):
    def __init__(self, tipo, modelo, km, portas):
        super().__init__(
            tipo, modelo, km
        )  # Chamando o construtor da superclasse
        self.portas = portas

    def exibe(self):
        print(
            f"{self._tipo} modelo {self.modelo} com {self.km} km rodados e {self.portas} portas."
        )


# Criando um objeto da subclasse
palio = Carro("Carro", "Palio", 10000, 2)
palio.exibe()
