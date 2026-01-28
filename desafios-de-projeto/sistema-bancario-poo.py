from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

# --- CLASSES DE TRANSAÇÃO ---


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


# --- CLASSE DE HISTÓRICO ---


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


# --- CLASSES DE CLIENTE ---


class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao: Transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(
        self, cpf: str, nome: str, data_nascimento: str, endereco: str
    ):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


# --- CLASSES DE CONTA ---


class Conta:
    def __init__(self, numero: int, cliente: Cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor: float) -> bool:
        if valor > self.saldo:
            print("\n@@@ Falha: Saldo insuficiente! @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. ===")
            return False


class ContaCorrente(Conta):
    def __init__(
        self, numero: int, cliente: Cliente, limite=500, limite_saques=3
    ):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        numero_saques = len(
            [t for t in self.historico.transacoes if t["tipo"] == "Saque"]
        )

        if valor > self.limite:
            print("\n@@@ Falha: O valor excede o limite do saque! @@@")
        elif numero_saques >= self.limite_saques:
            print("\n@@@ Falha: Limite de saques diários atingido! @@@")
        else:
            return super().sacar(valor)
        return False

    def __str__(self) -> str:
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


# --- INTEGRAÇÃO COM O MENU ---


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [c for c in clientes if c.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    return cliente.contas[0]  # Simplificação: retorna a primeira conta


def main():
    clientes = []
    contas = []

    while True:

        menu_texto = """\n
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nc]\tNova conta
        [lc]\tListar contas
        [nu]\tNovo usuário
        [q]\tSair
        => """
        opcao = input(textwrap.dedent(menu_texto))

        if opcao == "d":
            cpf = input("CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)
            if cliente:
                valor = float(input("Valor do depósito: "))
                transacao = Deposito(valor)
                conta = recuperar_conta_cliente(cliente)
                if conta:
                    cliente.realizar_transacao(conta, transacao)

        elif opcao == "s":
            cpf = input("CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)
            if cliente:
                valor = float(input("Valor do saque: "))
                transacao = Saque(valor)
                conta = recuperar_conta_cliente(cliente)
                if conta:
                    cliente.realizar_transacao(conta, transacao)

        elif opcao == "e":
            cpf = input("CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)
            if cliente:
                conta = recuperar_conta_cliente(cliente)
                if conta:
                    print("\n================ EXTRATO ================")
                    transacoes = conta.historico.transacoes
                    if not transacoes:
                        print("Não foram realizadas movimentações.")
                    else:
                        for t in transacoes:
                            print(f"{t['tipo']}:\tR$ {t['valor']:.2f}")
                    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")

        elif opcao == "nu":
            cpf = input("CPF: ")
            if filtrar_cliente(cpf, clientes):
                print("Cliente já existe!")
                continue
            nome = input("Nome: ")
            data = input("Data (dd-mm-aaaa): ")
            end = input("Endereço: ")
            clientes.append(
                PessoaFisica(
                    cpf=cpf, nome=nome, data_nascimento=data, endereco=end
                )
            )

        elif opcao == "nc":
            cpf = input("CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)
            if cliente:
                numero_conta = len(contas) + 1
                conta = ContaCorrente.nova_conta(cliente, numero_conta)
                contas.append(conta)
                cliente.adicionar_conta(conta)
                print("\n=== Conta criada com sucesso! ===")

        elif opcao == "lc":
            for conta in contas:
                print("=" * 30)
                print(
                    f"Agência:\t{conta.agencia}\nC/C:\t\t{conta.numero}\nTitular:\t{conta.cliente.nome}"
                )

        elif opcao == "q":
            break


if __name__ == "__main__":
    main()
