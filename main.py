import re

VALOER_LIMITE = 500
LIMITE_SAQUES = 3
USUARIO_DEFAULT = ['name', 'cpf', 'endereco']
CONTA_DEFAULT = ['usuario', 'agencia', 'conta',
                 'saldo', 'extrato', 'numero_saque']
usuarios = {}
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


def iniciarCriarUsuario():
    global usuarios

    usuario = dict.fromkeys(USUARIO_DEFAULT, "")

    cpf = input("Informe o seu cpf: ")

    if not validarCPF(cpf):
        print("Operação falhou! O CPF informado é inválido.")
        return iniciarCriarUsuario()

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

    usuarios[cpf] = {'nome': nome, 'cpf': cpf, 'endereco': endereco}
    print(usuarios)
    return


def iniciarCriarConta():
    return


def iniciarDepositar():
    global saldo
    global extrato

    valor = float(input("Informe o valor do depósito: "))

    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return

    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"


def iniciarSaque():
    global saldo
    global extrato
    global numero_saques
    valor = float(input("Informe o valor do saque: "))
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return

    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return

    if valor > VALOER_LIMITE:
        print("Operação falhou! O valor do saque excede o limite.")
        return

    if numero_saques >= LIMITE_SAQUES:
        print("Operação falhou! Número máximo de saques excedido.")
        return

    saldo -= valor
    extrato += f"Saque: R$ -{valor:.2f}\n"
    numero_saques += 1


def main():
    print("".center(50, "_"))
    MENU = {'1': {'title': 'Criar Usuario', 'function': iniciarCriarUsuario},
            '2': {'title': 'Criar Conta', 'function': iniciarCriarConta},
            '3': {'title': 'Depositar', 'function': iniciarDepositar},
            '4': {'title': 'Sacar', 'function': iniciarSaque},
            '5': {'title': 'Extrato', },
            's': {'title': 'Sair'}}

    for key, item in MENU.items():
        title = item.get('title', '').upper()
        print(f"[{key}] - {title}")

    opcao = input("=>")

    if opcao not in MENU.keys():
        print("Operação inválida, por favor selecione novamente a operação desejada.")

    if opcao in MENU.keys() and MENU[opcao].get('function', False):
        print(MENU.get(opcao).get('title').upper().center(50, "-"))
        MENU[opcao].get('function')()

    if opcao == "3":
        print("")
        print("EXTRATO".center(50, "="))
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("".center(50, "-"))

    if opcao != "s":
        main()


main()
