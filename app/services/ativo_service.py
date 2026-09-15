"""Regras de negócio relacionadas aos ativos de TI.

Além de validar os dados e delegar a gravação ao repositório, esta classe
mantém um cache em memória (um dicionário, indexado pelo id do ativo) com
todos os ativos cadastrados. Isso evita ter que consultar o banco de dados
toda vez que a interface gráfica precisa listar ou buscar um ativo,
otimizando as buscas conforme pedido nos requisitos RF10/RNF05.
"""

from typing import Dict, List

from app.exceptions import AtivoNaoEncontradoError, ErroDeValidacao
from app.models.ativo import Ativo
from app.models.enums import TipoAtivo
from app.repositories.ativo_repository import AtivoRepository


class AtivoService:
    """Camada de regras de negócio para cadastro, busca, edição e exclusão de ativos."""

    def __init__(self, repositorio_de_ativos: AtivoRepository):
        self._repositorio = repositorio_de_ativos
        self._ativos_por_id: Dict[int, Ativo] = {}
        self._recarregar_cache_a_partir_do_banco()

    def _recarregar_cache_a_partir_do_banco(self) -> None:
        ativos_cadastrados = self._repositorio.listar_todos()
        self._ativos_por_id = {ativo.id: ativo for ativo in ativos_cadastrados}

    def listar_todos(self) -> List[Ativo]:
        """Retorna todos os ativos cadastrados, ordenados por id."""
        return sorted(self._ativos_por_id.values(), key=lambda ativo: ativo.id)

    def buscar_por_id(self, ativo_id: int) -> Ativo:
        """Busca um ativo pelo identificador único, usando o cache em dicionário."""
        ativo = self._ativos_por_id.get(ativo_id)
        if ativo is None:
            raise AtivoNaoEncontradoError(f"Não existe ativo cadastrado com o ID {ativo_id}.")
        return ativo

    def buscar_por_nome(self, texto_buscado: str) -> List[Ativo]:
        """Busca ativos cujo nome/hostname contenha o texto informado."""
        termo_normalizado = texto_buscado.strip().lower()
        if not termo_normalizado:
            return self.listar_todos()

        return [
            ativo
            for ativo in self._ativos_por_id.values()
            if termo_normalizado in ativo.nome.lower()
        ]

    def cadastrar(
        self, nome: str, responsavel: str, setor: str, tipo: TipoAtivo, descricao: str = ""
    ) -> Ativo:
        """Valida e cadastra um novo ativo de TI."""
        self._validar_campos_obrigatorios(nome=nome, responsavel=responsavel, setor=setor)
        self._validar_tipo_de_ativo(tipo)

        novo_ativo = Ativo(
            nome=nome.strip(),
            responsavel=responsavel.strip(),
            setor=setor.strip(),
            tipo=tipo,
            descricao=descricao.strip(),
        )
        novo_ativo = self._repositorio.inserir(novo_ativo)
        self._ativos_por_id[novo_ativo.id] = novo_ativo
        return novo_ativo

    def atualizar(
        self,
        ativo_id: int,
        responsavel: str,
        setor: str,
        tipo: TipoAtivo,
        descricao: str = "",
    ) -> Ativo:
        """Valida e atualiza os dados de um ativo já cadastrado."""
        ativo_existente = self.buscar_por_id(ativo_id)
        self._validar_campos_obrigatorios(responsavel=responsavel, setor=setor)
        self._validar_tipo_de_ativo(tipo)

        ativo_existente.responsavel = responsavel.strip()
        ativo_existente.setor = setor.strip()
        ativo_existente.tipo = tipo
        ativo_existente.descricao = descricao.strip()

        self._repositorio.atualizar(ativo_existente)
        return ativo_existente

    def excluir(self, ativo_id: int) -> None:
        """Exclui um ativo do banco de dados (o banco remove em cascata as
        vulnerabilidades associadas a ele) e do cache em memória."""
        self.buscar_por_id(ativo_id)
        self._repositorio.excluir(ativo_id)
        del self._ativos_por_id[ativo_id]

    @staticmethod
    def _validar_campos_obrigatorios(**campos: str) -> None:
        for nome_do_campo, valor in campos.items():
            if valor is None or not str(valor).strip():
                raise ErroDeValidacao(f"O campo '{nome_do_campo}' é obrigatório.")

    @staticmethod
    def _validar_tipo_de_ativo(tipo: TipoAtivo) -> None:
        if not isinstance(tipo, TipoAtivo):
            raise ErroDeValidacao("Selecione um tipo de ativo válido.")
