ativos = ["Notebook", "Servidor", "Roteador", "Monitor"]

while True:
    print(" MENU - CONTROLE DE ATIVOS")
    print("1 - Listar ativos")
    print("2 - Procurar ativo")
    print("3 - Inserir ativo")
    print("4 - Remover ativo")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        print("Ativos disponíveis:")
        for ativo in ativos:
            print(ativo)
    elif opcao == "2":
        ativo = input("Digite o nome do ativo para busca: ")
        if ativo in ativos:
            index = ativos.index(ativo)
            print(f"Ativo {ativo} encontrado na posição {index}!")
        else:
            print(f"Ativo {ativo} não foi encontrado!")
    elif opcao == "3":
        ativo = input("Digite o nome do ativo para cadastrar: ")
        ativos.append(ativo)
        print(f"Ativo {ativo} cadastrado com sucesso!")
    elif opcao == "4":
        ativo = input("Digite o nome do ativo para remover: ")
        if ativo in ativos:
            ativos.remove(ativo)
            print(f"Ativo {ativo} removido com sucesso!")
        else:
            print(f"Ativo {ativo} não foi encontrado!")
    elif opcao == "0":
        print("Encerrando o programa.")
        break
    else:
        print("Opção inválida. Tente novamente.\n")
