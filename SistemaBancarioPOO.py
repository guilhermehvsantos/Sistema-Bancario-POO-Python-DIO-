import textwrap

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Conta:
    def __init__(self, cliente, numero, agencia):
        self.saldo = 0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.historico.adicionar_transacao(Deposito(valor))
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

    def sacar(self, valor, limite_saques):
        if valor <= self.saldo and limite_saques > 0:
            self.saldo -= valor
            self.historico.adicionar_transacao(Saque(valor))
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! Saldo insuficiente ou limite de saques excedido. @@@")
            return False


class Deposito:
    def __init__(self, valor):
        self.valor = valor


class Saque:
    def __init__(self, valor):
        self.valor = valor


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if isinstance(transacao, Transacao):
            transacao.registrar(conta)
        else:
            print("\n@@@ Transação inválida! @@@")
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia):
        super().__init__(cliente, numero, agencia)
        self.limite = 500
        self.limite_saques = 3

    def sacar(self, valor):
        return super().sacar(valor, self.limite_saques)


class DepositoTransacao(Transacao):
    def registrar(self, conta):
        pass  # Implementação do registro de depósito


class SaqueTransacao(Transacao):
    def registrar(self, conta):
        pass  # Implementação do registro de saque


def menu():
    menu_text = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_text))


def criar_conta(cliente, numero, agencia):
    return ContaCorrente(cliente, numero, agencia)


def criar_usuario():
    endereco = input("Informe o endereço: ")
    cpf = input("Informe o CPF: ")
    nome = input("Informe o nome: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    return PessoaFisica(endereco, cpf, nome, data_nascimento)


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(f"Agência:\t{conta.agencia}")
        print(f"C/C:\t\t{conta.numero}")
        print(f"Titular:\t{conta.cliente.nome}")


def main():
    AGENCIA = "0001"

    numero_conta = 1
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "nu":
            usuario = criar_usuario()
            usuarios.append(usuario)

        elif opcao == "nc":
            cliente = usuarios[-1] if usuarios else None
            if cliente:
                conta = criar_conta(cliente, numero_conta, AGENCIA)
                contas.append(conta)
                numero_conta += 1
                cliente.adicionar_conta(conta)
                print("\n=== Conta criada com sucesso! ===")
            else:
                print("\n@@@ Crie primeiro um usuário! @@@")
        
        elif opcao == "d":
            numero_conta = int(input("Informe o número da conta: "))
            valor = float(input("Informe o valor do depósito: "))

            for conta in contas:
                if conta.numero == numero_conta:
                    conta.depositar(valor)
                    break
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "s":
            numero_conta = int(input("Informe o número da conta: "))
            valor = float(input("Informe o valor do saque: "))

            for conta in contas:
                if conta.numero == numero_conta:
                    conta.sacar(valor)
                    break
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "e":
            numero_conta = int(input("Informe o número da conta: "))

            for conta in contas:
                if conta.numero == numero_conta:
                    print("\n================ EXTRATO ================")
                    # Aqui você deve percorrer o histórico da conta e exibir as transações
                    print("Extrato não implementado ainda.")
                    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
                    print("==========================================")
                    break
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
