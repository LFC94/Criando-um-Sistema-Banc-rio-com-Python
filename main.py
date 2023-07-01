import re

CENTER = 50
VALOER_LIMITE = 500
LIMITE_SAQUES = 3

AGENCIA = '0001'

usuarios = {'11235809609': {'nome': 'Lucas costa', 'cpf': '11235809609',
                            'endereco': 'topazio, 360 - pataf - para de minas/Mg'}}
contas = {}


def validarCPF(cpf: str) -> bool:

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais:
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True


def iniciarCriarUsuario(invalido=False):
    global usuarios
    sInvalido = ''
    if invalido:
        sInvalido = " (informe 's' para voltar ao Menu)"

    cpf = input(f"Informe o seu cpf{sInvalido}: ")

    if not validarCPF(cpf):
        print("Operação falhou! O CPF informado é inválido.")
        if cpf == 's':
            return

        return iniciarCriarUsuario(True)

    cpf = re.sub('[^0-9]', '', cpf)

    if cpf in usuarios.keys():
        print("Operação falhou! O CPF informado ja cadastrado.")
        return

    nome = input("Informe o seu nome: ")
    lagradouro = input("Informe o seu lagradouro(rua, avenida ...): ")
    numero = input("Informe o seu numero: ")
    bairo = input("Informe o seu bairo: ")
    cidade = input("Informe o seu cidade: ")
    sg = input("Informe o seu estado(sigla): ")

    endereco = f"{lagradouro}, {numero} - {bairo} - {cidade}/{sg}"

    usuarios[cpf] = {'nome': nome.upper(), 'cpf': cpf,
                     'endereco': endereco.upper()}
    print(usuarios)
    return


def validarUsuario(usuarios, /):
    cpf = input("Informe o seu cpf: ")
    if cpf not in usuarios.keys():
        print("Operação falhou! O CPF informado não esta cadastrado.")
        return False

    cpf = re.sub('[^0-9]', '', cpf)
    return cpf


def iniciarCriarConta():
    global contas
    global usuarios

    cpf = validarUsuario(usuarios)
    if (not cpf):
        return

    numeroConta = len(contas) + 1

    contas[numeroConta] = {'usuario': cpf, 'conta': numeroConta,
                           'agencia': AGENCIA, 'saldo': 0, 'extrato': [],
                           'numero_saque': 0}

    nome = usuarios[cpf].get('nome')

    print(f"\nOlá {nome} sua conta foi criada com sucesso")
    print(f"Agencia: {AGENCIA}")
    print(f"Conta: {numeroConta}\n")

    return


def listarContaUsuario():
    global contas
    global usuarios

    cpf = validarUsuario(usuarios)
    if (not cpf):
        return

    nome = usuarios[cpf].get('nome')

    print(f"\nOlá {nome} sua(s) conta(s):")

    semConta = True

    for conta in contas.values():
        if conta.get('usuario') == cpf:
            semConta = False
            print("".center(50, "_"))
            print(f"Agencia: {conta.get('agencia')}")
            print(f"Conta: {conta.get('conta')}")
            print(f"Saldo: R${conta.get('saldo'):.2f}")

    if semConta:
        print("Usuario não possui contas ativas")


def contaMovimentar(contas):
    agencia = input("Informe o sua agencia: ")
    conta = int(input("Informe o sua conta: "))

    if agencia != AGENCIA or conta not in contas.keys():
        print("Operação falhou! O Agencia ou Conta informado não esta cadastrado.")
        return False

    return contas[conta]


def getInformarValor(tipo: str):

    valor = float(input(f"Informe o valor do {tipo}: "))

    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return False

    return valor


def depositar(saldo, valor, extrato, /):

    saldo += valor
    extrato.append({"tipo": "Depósito", "valor": valor})

    return saldo, extrato


def iniciarDepositar():
    global contas
    conta = contaMovimentar(contas)
    if (not conta):
        return

    valor = getInformarValor('depositar')
    if not valor:
        return

    saldo, extrato = depositar(conta.get('saldo'), valor, conta.get('extrato'))

    conta['saldo'] = saldo
    conta['extrato'] = extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return saldo, extrato

    if valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
        return saldo, extrato

    if numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        return saldo, extrato

    saldo -= valor
    extrato.append({"tipo": "Saque", "valor": valor})

    return saldo, extrato


def iniciarSaque():
    global contas
    conta = contaMovimentar(contas)
    if (not conta):
        return

    valor = getInformarValor('sacar')
    if not valor:
        return

    numero_saques = conta.get('numero_saque') + 1

    saldo, extrato = sacar(saldo=conta.get('saldo'),
                           valor=valor,
                           extrato=conta.get('extrato'),
                           numero_saques=numero_saques,
                           limite=VALOER_LIMITE,
                           limite_saques=LIMITE_SAQUES)

    conta['saldo'] = saldo
    conta['extrato'] = extrato
    conta['numero_saques'] = numero_saques


def main():
    print("".center(50, "_"))
    print(" MENU ".center(CENTER, "-") + "\n")
    MENU = {'1': {'title': 'Criar Usuario', 'function': iniciarCriarUsuario},
            '2': {'title': 'Criar Conta', 'function': iniciarCriarConta},
            '3': {'title': 'Listar Conta', 'function': listarContaUsuario},
            '4': {'title': 'Depositar', 'function': iniciarDepositar},
            '5': {'title': 'Sacar', 'function': iniciarSaque},
            '6': {'title': 'Extrato', },
            's': {'title': 'Sair'}}

    for key, item in MENU.items():
        title = item.get('title', '').upper()
        print(f"[{key}] - {title}")

    opcao = input("\n=>")

    if opcao not in MENU.keys():
        print("Operação inválida, por favor selecione novamente a operação desejada.")

    if opcao in MENU.keys() and MENU[opcao].get('function', False):
        print(MENU.get(opcao).get('title').upper().center(CENTER, "-"))
        MENU[opcao].get('function')()

    # if opcao == "3":
    #     print("")
    #     print("EXTRATO".center(CENTER, "="))
    #     print("Não foram realizadas movimentações." if not extrato else extrato)
    #     print(f"\nSaldo: R$ {saldo:.2f}")
    #     print("".center(CENTER, "-"))

    if opcao != "s":
        main()


main()
