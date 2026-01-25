"""
Sistema Bancário - Versão 2

Este módulo implementa um sistema bancário simples em Python, com as seguintes
funcionalidades:
    - Cadastro de clientes (usuários do banco)
    - Criação de contas correntes vinculadas a clientes
    - Operações de depósito, saque e extrato

Regras de negócio:
    - Funções seguem padrões específicos de passagem de argumentos:
        - saque: argumentos apenas por nome (keyword only)
        - depositar: argumentos apenas por posição (positional only)
        - extrato: argumentos por posição e nome (positional only e keyword only)
    - Limite de 3 saques diários
    - Limite de R$ 500,00 por saque
    - CPF único por cliente
    - Cliente pode ter múltiplas contas, mas conta pertence a um único cliente
    - Número da agência fixo: "0001"
    - Número da conta sequencial, iniciando em 1

Autor: [Seu Nome]
Data: Janeiro/2025
"""

from typing import Optional

# =============================================================================
# CONSTANTES DO SISTEMA
# =============================================================================

LIMITE_SAQUES_DIARIOS: int = 3
LIMITE_VALOR_SAQUE: float = 500.0
NUMERO_AGENCIA: str = "0001"

# =============================================================================
# MENU DO SISTEMA
# =============================================================================

MENU_PRINCIPAL: str = """
╔══════════════════════════════════════╗
║       SISTEMA BANCÁRIO v2.0          ║
╠══════════════════════════════════════╣
║  [cc] Cadastrar cliente              ║
║  [cr] Criar conta corrente           ║
║  [l]  Listar clientes cadastrados    ║
║  [d]  Depositar                      ║
║  [s]  Sacar                          ║
║  [e]  Extrato                        ║
║  [q]  Sair                           ║
╚══════════════════════════════════════╝

=> """

# =============================================================================
# VARIÁVEIS GLOBAIS (Estado do Sistema)
# =============================================================================

saldo_conta: float = 0.0
historico_transacoes: str = ""
quantidade_saques_realizados: int = 0

# Lista de clientes cadastrados no sistema
# Cada cliente é um dicionário com: nome, data_nascimento, cpf, endereco
lista_clientes_cadastrados: list[dict] = [
    {
        "nome_completo": "Eric Moniz",
        "data_nascimento": "00/00/0000",
        "cpf": "1234",
        "endereco_completo": "rua do cipreste, 85 - vila do matão - são paulo/sp",
    },
    {
        "nome_completo": "Jose Pele",
        "data_nascimento": "00/00/0000",
        "cpf": "12",
        "endereco_completo": "rua do cipreste, 85 - vila do matão - são paulo/sp",
    },
]

# Lista de contas correntes criadas
# Cada conta é um dicionário com: agencia, numero_conta, cpf_titular
lista_contas_correntes: list[dict] = []


# =============================================================================
# FUNÇÕES DE OPERAÇÕES BANCÁRIAS
# =============================================================================


def realizar_deposito(
    saldo_atual: float,
    valor_deposito: float,
    historico_atual: str,
    /,
) -> tuple[float, str]:
    """
    Realiza um depósito na conta do cliente.

    Esta função recebe argumentos apenas por posição (positional only),
    conforme indicado pela barra (/) na assinatura.

    Args:
        saldo_atual: Saldo atual da conta antes do depósito.
        valor_deposito: Valor a ser depositado (deve ser positivo).
        historico_atual: Histórico de transações atual.

    Returns:
        tuple: Contendo o novo saldo e o histórico atualizado.

    Exemplo:
        >>> novo_saldo, historico = realizar_deposito(100.0, 50.0, "")
        >>> print(novo_saldo)
        150.0
    """
    if valor_deposito > 0:
        saldo_atualizado = saldo_atual + valor_deposito
        historico_atualizado = historico_atual + f"Depósito: R$ {valor_deposito:.2f}\n"
        return saldo_atualizado, historico_atualizado

    print("❌ Operação falhou! O valor informado é inválido.")
    return saldo_atual, historico_atual


def realizar_saque(
    *,
    saldo_atual: float,
    valor_saque: float,
    historico_atual: str,
    limite_por_saque: float,
    saques_realizados: int,
    limite_quantidade_saques: int,
) -> tuple[float, str, int]:
    """
    Realiza um saque na conta do cliente.

    Esta função recebe argumentos apenas por nome (keyword only),
    conforme indicado pelo asterisco (*) na assinatura.

    Validações realizadas:
        - Verifica se há saldo suficiente
        - Verifica se o valor não excede o limite por saque
        - Verifica se não excedeu o limite de saques diários
        - Verifica se o valor é positivo

    Args:
        saldo_atual: Saldo atual da conta.
        valor_saque: Valor a ser sacado.
        historico_atual: Histórico de transações atual.
        limite_por_saque: Valor máximo permitido por saque.
        saques_realizados: Quantidade de saques já realizados no dia.
        limite_quantidade_saques: Quantidade máxima de saques permitidos.

    Returns:
        tuple: Contendo o novo saldo, histórico atualizado e quantidade
               de saques realizados.

    Exemplo:
        >>> saldo, hist, saques = realizar_saque(
        ...     saldo_atual=1000.0,
        ...     valor_saque=100.0,
        ...     historico_atual="",
        ...     limite_por_saque=500.0,
        ...     saques_realizados=0,
        ...     limite_quantidade_saques=3
        ... )
    """
    # Validações de regras de negócio
    saldo_insuficiente = valor_saque > saldo_atual
    excedeu_limite_valor = valor_saque > limite_por_saque
    excedeu_limite_quantidade = saques_realizados >= limite_quantidade_saques

    if saldo_insuficiente:
        print("❌ Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite_valor:
        print(
            f"❌ Operação falhou! O valor do saque excede o limite de R$ {limite_por_saque:.2f}."
        )
    elif excedeu_limite_quantidade:
        print(
            f"❌ Operação falhou! Limite de {limite_quantidade_saques} saques diários excedido."
        )
    elif valor_saque > 0:
        # Saque aprovado
        saldo_atualizado = saldo_atual - valor_saque
        historico_atualizado = historico_atual + f"Saque:    R$ {valor_saque:.2f}\n"
        saques_realizados += 1
        return saldo_atualizado, historico_atualizado, saques_realizados
    else:
        print("❌ Operação falhou! O valor informado é inválido.")

    # Retorna valores inalterados em caso de falha
    return saldo_atual, historico_atual, saques_realizados


def exibir_extrato(saldo_atual: float, /, *, historico: str) -> None:
    """
    Exibe o extrato bancário do cliente.

    Esta função recebe argumentos por posição e nome:
        - saldo_atual: argumento posicional (positional only)
        - historico: argumento nomeado (keyword only)

    Args:
        saldo_atual: Saldo atual da conta (positional only).
        historico: Histórico de transações (keyword only).

    Returns:
        None: Apenas imprime o extrato na tela.
    """
    linha_separadora = "=" * 42

    print(f"\n{linha_separadora}")
    print("              📄 EXTRATO BANCÁRIO")
    print(linha_separadora)

    if not historico:
        print("Não foram realizadas movimentações.")
    else:
        print(historico)

    print(linha_separadora)
    print(f"💰 Saldo atual: R$ {saldo_atual:.2f}")
    print(linha_separadora)


# FUNÇÕES DE GERENCIAMENTO DE CLIENTES


def buscar_cliente_por_cpf(
    lista_clientes: list[dict], cpf_busca: str
) -> Optional[dict]:
    """
    Busca um cliente na lista pelo número do CPF.

    Args:
        lista_clientes: Lista contendo todos os clientes cadastrados.
        cpf_busca: CPF a ser pesquisado (somente números).

    Returns:
        dict: Dados do cliente se encontrado.
        None: Se o cliente não foi encontrado.

    Exemplo:
        >>> cliente = buscar_cliente_por_cpf(clientes, "12345678900")
        >>> if cliente:
        ...     print(cliente["nome_completo"])
    """
    for cliente in lista_clientes:
        if cpf_busca == cliente["cpf"]:
            return cliente

    return None


def verificar_cpf_cadastrado(lista_clientes: list[dict], cpf: str) -> bool:
    """
    Verifica se um CPF já está cadastrado no sistema.

    Args:
        lista_clientes: Lista contendo todos os clientes cadastrados.
        cpf: CPF a ser verificado.

    Returns:
        bool: True se o CPF já existe, False caso contrário.
    """
    return buscar_cliente_por_cpf(lista_clientes, cpf) is not None


def cadastrar_novo_cliente(lista_clientes: list[dict]) -> Optional[dict]:
    """
    Cadastra um novo cliente no sistema bancário.

    Solicita os dados do cliente via input e valida se o CPF já está
    cadastrado. Um cliente é composto por:
        - Nome completo
        - Data de nascimento
        - CPF (somente números)
        - Endereço (formato: logradouro, número - bairro - cidade/UF)

    Args:
        lista_clientes: Lista de clientes para verificar CPF duplicado.

    Returns:
        dict: Dicionário com os dados do novo cliente.
        None: Se o CPF já estiver cadastrado.
    """
    print("\n" + "=" * 40)
    print("      📝 CADASTRO DE NOVO CLIENTE")
    print("=" * 40)

    cpf_informado = input("Digite o CPF (somente números): ").strip()

    # Verifica se o CPF já está cadastrado
    if verificar_cpf_cadastrado(lista_clientes, cpf_informado):
        print("❌ CPF já cadastrado no sistema!")
        return None

    # Coleta os dados do cliente
    nome_informado = input("Nome completo: ").strip()
    nascimento_informado = input("Data de nascimento (dd/mm/aaaa): ").strip()

    print("Digite o endereço completo")
    print("(formato: logradouro, número - bairro - cidade/UF)")
    endereco_informado = input(": ").strip()

    # Cria o dicionário do cliente
    novo_cliente = {
        "nome_completo": nome_informado,
        "data_nascimento": nascimento_informado,
        "cpf": cpf_informado,
        "endereco_completo": endereco_informado,
    }

    print("✅ Cliente cadastrado com sucesso!")
    return novo_cliente


def listar_todos_clientes(lista_clientes: list[dict]) -> None:
    """
    Exibe uma tabela formatada com todos os clientes cadastrados.

    Args:
        lista_clientes: Lista contendo todos os clientes cadastrados.

    Returns:
        None: Apenas imprime a tabela na tela.
    """
    if not lista_clientes:
        print("\n⚠️ Nenhum cliente cadastrado no sistema.")
        return

    # Larguras das colunas
    largura_id = 4
    largura_nome = 21
    largura_nascimento = 12
    largura_cpf = 14
    largura_endereco = 62

    # Linha separadora
    linha_divisoria = (
        f"+{'-' * largura_id}"
        f"+{'-' * largura_nome}"
        f"+{'-' * largura_nascimento}"
        f"+{'-' * largura_cpf}"
        f"+{'-' * largura_endereco}+"
    )

    print(f"\n{linha_divisoria}")
    print(
        f"| {'Id':^{largura_id - 1}}"
        f"| {'Nome':<{largura_nome - 1}}"
        f"| {'Data Nasc.':<{largura_nascimento - 1}}"
        f"| {'CPF':<{largura_cpf - 1}}"
        f"| {'Endereço':<{largura_endereco - 1}}|"
    )

    for indice, cliente in enumerate(lista_clientes, start=1):
        print(linha_divisoria)
        print(
            f"| {indice:<{largura_id - 1}}"
            f"| {cliente['nome_completo']:<{largura_nome - 1}}"
            f"| {cliente['data_nascimento']:<{largura_nascimento - 1}}"
            f"| {cliente['cpf']:<{largura_cpf - 1}}"
            f"| {cliente['endereco_completo']:<{largura_endereco - 1}}|"
        )

    print(linha_divisoria)
    print(f"\n📊 Total de clientes: {len(lista_clientes)}")


# FUNÇÕES DE GERENCIAMENTO DE CONTAS


def obter_proximo_numero_conta(lista_contas: list[dict]) -> int:
    """
    Determina o próximo número de conta disponível.

    Percorre a lista de contas existentes e retorna o próximo número
    sequencial.

    Args:
        lista_contas: Lista de contas correntes existentes.

    Returns:
        int: Próximo número de conta disponível.
    """
    if not lista_contas:
        return 1

    maior_numero = max(conta["numero_conta"] for conta in lista_contas)
    return maior_numero + 1


def criar_nova_conta(
    lista_contas: list[dict],
    lista_clientes: list[dict],
) -> Optional[dict]:
    """
    Cria uma nova conta corrente vinculada a um cliente existente.

    Uma conta é composta por:
        - Agência (fixo: "0001")
        - Número da conta (sequencial, iniciando em 1)
        - CPF do titular

    Regras:
        - O cliente deve estar previamente cadastrado
        - Um cliente pode ter múltiplas contas
        - Uma conta pertence a apenas um cliente

    Args:
        lista_contas: Lista de contas para obter o próximo número.
        lista_clientes: Lista de clientes para validar o CPF.

    Returns:
        dict: Dicionário com os dados da nova conta.
        None: Se o cliente não estiver cadastrado.
    """
    print("\n" + "=" * 40)
    print("      🏦 CRIAR CONTA CORRENTE")
    print("=" * 40)

    cpf_titular = input("Digite o CPF do titular (somente números): ").strip()

    # Verifica se o cliente existe
    if not verificar_cpf_cadastrado(lista_clientes, cpf_titular):
        print("❌ Cliente não encontrado! Cadastre o cliente primeiro.")
        return None

    # Gera o número da nova conta
    numero_nova_conta = obter_proximo_numero_conta(lista_contas)

    # Cria o dicionário da conta
    nova_conta = {
        "agencia": NUMERO_AGENCIA,
        "numero_conta": numero_nova_conta,
        "cpf_titular": cpf_titular,
    }

    print("✅ Conta criada com sucesso!")
    print(f"   Agência: {NUMERO_AGENCIA}")
    print(f"   Conta: {numero_nova_conta}")

    return nova_conta


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================


def main() -> None:
    """
    Função principal que executa o loop do sistema bancário.

    Gerencia o menu principal e direciona para as operações
    correspondentes baseado na escolha do usuário.
    """
    # Referencia as variáveis globais que serão modificadas
    global saldo_conta, historico_transacoes, quantidade_saques_realizados

    while True:
        opcao_selecionada = input(MENU_PRINCIPAL).strip().lower()

        match opcao_selecionada:
            case "cc":
                # Cadastrar novo cliente
                novo_cliente = cadastrar_novo_cliente(lista_clientes_cadastrados)
                if novo_cliente:
                    lista_clientes_cadastrados.append(novo_cliente)

            case "cr":
                # Criar nova conta corrente
                nova_conta = criar_nova_conta(
                    lista_contas_correntes,
                    lista_clientes_cadastrados,
                )
                if nova_conta:
                    lista_contas_correntes.append(nova_conta)

            case "d":
                # Realizar depósito
                try:
                    valor_informado = float(input("Informe o valor do depósito: R$ "))
                    saldo_conta, historico_transacoes = realizar_deposito(
                        saldo_conta,
                        valor_informado,
                        historico_transacoes,
                    )
                except ValueError:
                    print("❌ Valor inválido! Digite um número válido.")

            case "s":
                # Realizar saque
                try:
                    valor_informado = float(input("Informe o valor do saque: R$ "))
                    saldo_conta, historico_transacoes, quantidade_saques_realizados = (
                        realizar_saque(
                            saldo_atual=saldo_conta,
                            valor_saque=valor_informado,
                            historico_atual=historico_transacoes,
                            limite_por_saque=LIMITE_VALOR_SAQUE,
                            saques_realizados=quantidade_saques_realizados,
                            limite_quantidade_saques=LIMITE_SAQUES_DIARIOS,
                        )
                    )
                except ValueError:
                    print("❌ Valor inválido! Digite um número válido.")

            case "e":
                # Exibir extrato
                exibir_extrato(saldo_conta, historico=historico_transacoes)

            case "l":
                # Listar clientes cadastrados
                listar_todos_clientes(lista_clientes_cadastrados)

            case "q":
                # Sair do sistema
                print("\n👋 Obrigado por utilizar nosso sistema. Até logo!")
                break

            case _:
                # Opção inválida
                print("❌ Opção inválida! Selecione uma opção do menu.")


if __name__ == "__main__":
    main()
