ativos = ["Notebook", "Servidor", "Roteador", "Monitor"]

while True:
    print(" MENU - CLASSIFICAÇÃO DE VULNERABILIDADES")
    print("1 - Listar ativos")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        print("Ativos disponíveis:")
        for ativo in ativos:
            print(ativo)
    elif opcao == "0":
        print("Encerrando o programa.")
        break
    else:
        print("Opção inválida. Tente novamente.\n")
