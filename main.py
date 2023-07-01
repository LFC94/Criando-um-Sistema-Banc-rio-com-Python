
VALOER_LIMITE = 500
LIMITE_SAQUES = 3
saldo = 0
extrato = ""
numero_saques = 0


def depositar():
    global saldo
    global extrato

    valor = float(input("Informe o valor do depósito: "))

    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return

    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"


def sacar():
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
    MENU = {'1': {'title': 'Depositar', 'function': depositar},
            '2': {'title': 'Sacar', 'function': sacar},
            '3': {'title': 'Extrato', },
            's': {'title': 'Sair'}}

    for key, item in MENU.items():
        title = item.get('title', '').upper()
        print(f"[{key}] - {title}")
    opcao = input("=>")
    print("".center(50, "_"))

    if opcao not in MENU.keys():
        print("Operação inválida, por favor selecione novamente a operação desejada.")

    if opcao in MENU.keys() and MENU[opcao].get('function', False):
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
