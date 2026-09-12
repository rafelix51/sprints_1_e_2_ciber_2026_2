ativos = {}  # dict: {id_ativo: {"nome":..., "responsavel":..., "vulnerabilidades": [...]}}

def campo_obrigatorio_valido(valor: str) -> bool:
    return valor is not None and valor.strip() != ""


def obter_classificacao_severidade(severidade: int) -> str:
    if severidade >= 9:
        return "Crítica"
    elif 7 <= severidade <= 8:
        return "Alta"
    elif 4 <= severidade <= 6:
        return "Média"
    else:
        return "Baixa"

def exibir_ativo_simples(nome: str, responsavel: str) -> None:
    print(f"Ativo: {nome}  |  Responsável: {responsavel}")


def exibir_ativo_completo(id_ativo: int, dados: dict) -> None:
    print("-" * 45)
    print(f"ID.........: {id_ativo}")
    print(f"Nome/Host..: {dados['nome']}")
    print(f"Responsável: {dados['responsavel']}")

    vulns = dados["vulnerabilidades"]
    if not vulns:
        print("Vulnerabilidades: nenhuma registrada.")
    else:
        print(f"Vulnerabilidades ({len(vulns)}):")
        for i, v in enumerate(vulns, start=1):
            print(f"  {i}. {v['descricao']} | Severidade: {v['severidade']} | Status: {v['status']}")
    print("-" * 45)


def registrar_vulnerabilidade(descricao: str, categoria: str, severidade: str, status: str) -> dict:
    return {
        "descricao": descricao,
        "categoria": categoria,
        "severidade": severidade,
        "status": status,
    }


def acao_cadastrar_ativo() -> None:
    id_texto = input("ID do ativo (número inteiro): ").strip()
    if not id_texto.isdigit():
        print("Erro: o ID deve ser um número inteiro.\n")
        return
    id_ativo = int(id_texto)

    if id_ativo in ativos:
        print(f"Erro: já existe um ativo cadastrado com o ID {id_ativo}.\n")
        return

    nome = input("Nome/hostname do ativo: ")
    responsavel = input("Responsável pelo ativo: ")

    if not campo_obrigatorio_valido(nome) or not campo_obrigatorio_valido(responsavel):
        print("Erro: nome e responsável são obrigatórios e não podem ficar vazios.\n")
        return

    ativos[id_ativo] = {
        "nome": nome.strip(),
        "responsavel": responsavel.strip(),
        "vulnerabilidades": [],
    }

    print("\nAtivo cadastrado com sucesso!")
    exibir_ativo_simples(nome, responsavel)
    print()


def acao_cadastrar_vulnerabilidade() -> None:
    id_texto = input("ID do ativo que receberá a vulnerabilidade: ").strip()
    if not id_texto.isdigit() or int(id_texto) not in ativos:
        print("Erro: ativo não encontrado. Cadastre o ativo antes.\n")
        return
    id_ativo = int(id_texto)

    descricao = input("Descrição da vulnerabilidade: ")
    categoria = input("Categoria (ex.: senha fraca, software desatualizado): ")
    severidade = int(input("Severidade (inteiro entre 1 e 10): "))
    classificacao = obter_classificacao_severidade(severidade)
    status = input("Status (aberta, em tratamento, corrigida, aceita como risco): ")

    campos = [descricao, categoria, classificacao, status]
    if not all(campo_obrigatorio_valido(c) for c in campos):
        print("Erro: todos os campos da vulnerabilidade são obrigatórios.\n")
        return

    nova_vulnerabilidade = registrar_vulnerabilidade(descricao, categoria, classificacao, status)
    ativos[id_ativo]["vulnerabilidades"].append(nova_vulnerabilidade)

    print(f"\nVulnerabilidade registrada com sucesso.\n")


def acao_consultar_ativo() -> None:
    id_texto = input("ID do ativo a consultar: ").strip()
    if not id_texto.isdigit() or int(id_texto) not in ativos:
        print("Erro: ativo não encontrado.\n")
        return
    id_ativo = int(id_texto)
    exibir_ativo_completo(id_ativo, ativos[id_ativo])
    print()


def exibir_menu() -> None:
    print("=" * 50)
    print(" MENU - INVENTÁRIO DE ATIVOS E VULNERABILIDADES")
    print("=" * 50)
    print("1 - Cadastrar ativo")
    print("2 - Cadastrar vulnerabilidade em um ativo")
    print("3 - Consultar ativo (com vulnerabilidades)")
    print("0 - Sair")
    print("=" * 50)


def main() -> None:
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            acao_cadastrar_ativo()
        elif opcao == "2":
            acao_cadastrar_vulnerabilidade()
        elif opcao == "3":
            acao_consultar_ativo()
        elif opcao == "0":
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.\n")


if __name__ == "__main__":
    main()