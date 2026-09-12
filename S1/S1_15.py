import json
import os

ARQUIVO_DADOS = "ativo.json"


class DadosInvalidosError(Exception):
    """Levantada quando os dados informados pelo usuário são inválidos."""


class PersistenciaError(Exception):
    """Levantada quando há falha ao ler ou gravar o arquivo de dados."""


def campo_obrigatorio_valido(valor: str) -> bool:
    return valor is not None and valor.strip() != ""


def carregar_ativo() -> dict:
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError as erro:
            raise PersistenciaError(
                f"O arquivo '{ARQUIVO_DADOS}' está corrompido ou não é um JSON válido."
            ) from erro
        except OSError as erro:
            raise PersistenciaError(
                f"Não foi possível ler o arquivo '{ARQUIVO_DADOS}': {erro}"
            ) from erro

    return {
        "nome": "DB-Server-01",
        "ip": "192.168.1.10",
        "sistema_operacional": "Ubuntu Server 24.04",
        "criticidade": "alta",
    }


def salvar_ativo(ativo: dict) -> None:
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(ativo, arquivo, ensure_ascii=False, indent=4)
    except OSError as erro:
        raise PersistenciaError(
            f"Não foi possível salvar o arquivo '{ARQUIVO_DADOS}': {erro}"
        ) from erro


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
        raise DadosInvalidosError("todos os campos são obrigatórios.")

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
        raise DadosInvalidosError(
            f"nenhuma vulnerabilidade encontrada com a descrição '{descricao}'."
        )

    novo_status = input("Novo status (aberta, em tratamento, corrigida, aceita como risco): ")
    if not campo_obrigatorio_valido(novo_status):
        raise DadosInvalidosError("o status não pode ficar vazio.")

    vulnerabilidades[descricao]["status"] = novo_status
    salvar_ativo(ativo)
    print(f"Vulnerabilidade '{descricao}' atualizada para status '{novo_status}'.\n")


if __name__ == "__main__":
    try:
        ativo = carregar_ativo()
    except PersistenciaError as erro:
        print(f"Erro ao carregar dados: {erro}\n")
        raise SystemExit(1) from erro

    while True:
        print(" MENU - CONTROLE DE VULNERABILIDADES")
        print("1 - Listar ativos")
        print("2 - Cadastrar vulnerabilidade")
        print("3 - Atualizar vulnerabilidade")
        print("0 - Sair")

        try:
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
        except DadosInvalidosError as erro:
            print(f"Erro: {erro}\n")
        except PersistenciaError as erro:
            print(f"Erro ao salvar dados: {erro}\n")
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada interrompida. Encerrando o programa.")
            break
