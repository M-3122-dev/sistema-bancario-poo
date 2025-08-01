from abc import ABC, abstractmethod
from datetime import datetime

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        transacao_registrada = {
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        self._transacoes.append(transacao_registrada)

    @property
    def transacoes(self):
        return self._transacoes

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
            print(f" Saque de R${self.valor:.2f} realizado com sucesso.")
        else:
            print(f" Saque de R${self.valor:.2f} falhou.")

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
            print(f"Depósito de R${self.valor:.2f} realizado com sucesso.")
        else:
            print(f"Depósito de R${self.valor:.2f} falhou.")

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        super().__init__(endereco)

class Conta:
    def __init__(self, cliente, numero, agencia, saldo=0):
        self.cliente = cliente
        self.numero = numero
        self.agencia = agencia
        self._saldo = saldo
        self.historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    def sacar(self, valor):
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            return True
        else:
            print(" Saque não permitido: saldo insuficiente ou valor inválido.")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True
        else:
            print(" Depósito inválido.")
            return False

    @classmethod
    def nova_conta(cls, cliente, numero):
        conta = cls(cliente=cliente, numero=numero, agencia="0001")
        cliente.adicionar_conta(conta)
        return conta

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia, saldo=0, limite=500, limite_saques=3):
        super().__init__(cliente, numero, agencia, saldo)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        saques_realizados = [t for t in self.historico.transacoes if t["tipo"] == "Saque"]

        if len(saques_realizados) >= self.limite_saques:
            print(" Limite de saques diários atingido.")
            return False

        if valor > (self._saldo + self.limite):
            print(" Valor excede o limite disponível (saldo + limite).")
            return False

        self._saldo -= valor
        return True

# ---------------- FUNÇÃO PRINCIPAL --------------------

def main():
    print("🏦 Bem-vindo ao sistema bancário com POO!\n")

    # Criar cliente
    cliente1 = PessoaFisica(
        nome="José Mateus",
        cpf="123.456.789-00",
        data_nascimento="01/01/2000",
        endereco="Rua das Palmeiras, 123"
    )

    # Criar conta corrente
    conta1 = ContaCorrente(cliente=cliente1, numero=1001, agencia="0001")
    cliente1.adicionar_conta(conta1)

    # Depósito de R$1000
    deposito = Deposito(1000)
    cliente1.realizar_transacao(conta1, deposito)

    # Dois saques válidos
    saque1 = Saque(200)
    cliente1.realizar_transacao(conta1, saque1)

    saque2 = Saque(100)
    cliente1.realizar_transacao(conta1, saque2)

    # Saque que ultrapassa o saldo
    saque_invalido = Saque(2000)
    cliente1.realizar_transacao(conta1, saque_invalido)

    # Terceiro saque válido (atinge o limite de 3 saques)
    saque3 = Saque(50)
    cliente1.realizar_transacao(conta1, saque3)

    # Quarto saque excede o limite de saques
    saque4 = Saque(30)
    cliente1.realizar_transacao(conta1, saque4)

    # Exibir dados
    print("\nExtrato da Conta:")
    print(f"Cliente: {cliente1.nome}")
    print(f"CPF: {cliente1.cpf}")
    print(f"Número da conta: {conta1.numero}")
    print(f"Agência: {conta1.agencia}")
    print(f"Saldo atual: R${conta1.saldo:.2f}")

    print("\n Histórico de Transações:")
    for transacao in conta1.historico.transacoes:
        print(f"{transacao['data']} - {transacao['tipo']}: R${transacao['valor']:.2f}")

# Executar
if __name__ == "__main__":
    main()
