# 9 e 10: critica; 7 e 8: alta; 4, 5 e 6: média; 1, 2 e 3: baixa
while True:
    print(" MENU - CLASSIFICAÇÃO DE VULNERABILIDADES")
    print("1 - Cadastrar vulnerabilidade")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ").strip()
    classificacao = ""

    if opcao == "1":
        severidade = int(input("Digite a severidade da vulnerabilidade (entre 1 e 10): "))
        if severidade is not None and severidade > 0 and severidade < 11:
            if severidade >= 9:
                classificacao = "Crítica"
            elif 7 <= severidade <= 8:
                classificacao = "Alta"
            elif 4 <= severidade <= 6:
                classificacao = "Média"
            else:
                classificacao = "Baixa"
        else:
            print("Erro: a severidade deve ser entre 1 e 10.\n")
            continue

        print(f"Classificação: {classificacao} ({severidade})")
    elif opcao == "0":
        print("Encerrando o programa.")
        break
    else:
        # Tratamento de erro para opção inválida do menu
        print("Opção inválida. Tente novamente.\n")
