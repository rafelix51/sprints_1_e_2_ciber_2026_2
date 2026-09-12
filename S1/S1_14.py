import json
import os

ARQUIVO_DADOS = "ativo.json"


def campo_obrigatorio_valido(valor: str) -> bool:
    return valor is not None and valor.strip() != ""


def carregar_ativo() -> dict:
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    return {
        "nome": "DB-Server-01",
        "ip": "192.168.1.10",
        "sistema_operacional": "Ubuntu Server 24.04",
        "criticidade": "alta",
    }


def salvar_ativo(ativo: dict) -> None:
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(ativo, arquivo, ensure_ascii=False, indent=4)


def cadastrar_vulnerabilidade(ativo: dict) -> None:
    """
    Adiciona uma nova vulnerabilidade ao ativo. As vulnerabilidades ficam
    guardadas em um dicionário interno, indexado pela descrição, o que
    facilita localizar e atualizar uma vulnerabilidade específica depois.
    """
    if "vulnerabilidades" not in ativo:
        ativo["vulnerabilidades"] = {}
 
    descricao = input("Descrição da vulnerabilidade: ")
    severidade = input("Severidade (baixa, média, alta, crítica): ")
    status = input("Status (aberta, em tratamento, corrigida, aceita como risco): ")
 
    if not all(campo_obrigatorio_valido(c) for c in (descricao, severidade, status)):
        print("Erro: todos os campos são obrigatórios.\n")
        return
 
    ativo["vulnerabilidades"][descricao] = {
        "severidade": severidade,
        "status": status,
    }
    salvar_ativo(ativo)
    print(f"Vulnerabilidade '{descricao}' cadastrada com sucesso.\n")
 
 
def atualizar_vulnerabilidade(ativo: dict) -> None:
    """
    Atualiza o status (ou severidade) de uma vulnerabilidade já existente
    no dicionário 'vulnerabilidades' do ativo.
    """
    vulnerabilidades = ativo.get("vulnerabilidades", {})
    if not vulnerabilidades:
        print("Este ativo ainda não possui vulnerabilidades cadastradas.\n")
        return
 
    descricao = input("Descrição da vulnerabilidade a atualizar: ")
    if descricao not in vulnerabilidades:
        print(f"Erro: nenhuma vulnerabilidade encontrada com a descrição '{descricao}'.\n")
        return
 
    novo_status = input("Novo status (aberta, em tratamento, corrigida, aceita como risco): ")
    if not campo_obrigatorio_valido(novo_status):
        print("Erro: o status não pode ficar vazio.\n")
        return
 
    vulnerabilidades[descricao]["status"] = novo_status
    salvar_ativo(ativo)
    print(f"Vulnerabilidade '{descricao}' atualizada para status '{novo_status}'.\n")


if __name__ == "__main__":
    ativo = carregar_ativo()

    while True:
        print(" MENU - CONTROLE DE VULNERABILIDADES")
        print("1 - Listar ativos")
        print("2 - Cadastrar vulnerabilidade")
        print("3 - Atualizar vulnerabilidade")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print(ativo)
        elif opcao == "2":
            cadastrar_vulnerabilidade(ativo)
        elif opcao == "3":
            atualizar_vulnerabilidade(ativo)
        elif opcao == "0":
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Tente novamente.\n")
