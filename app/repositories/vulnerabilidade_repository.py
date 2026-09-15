"""Repositório responsável pelas operações de CRUD da tabela 'vulnerabilidades'."""

import sqlite3
from typing import List, Optional

from app.models.enums import Severidade, StatusVulnerabilidade
from app.models.vulnerabilidade import Vulnerabilidade
from app.repositories.database import ConexaoBancoDeDados


class VulnerabilidadeRepository:
    """Traduz operações de CRUD de Vulnerabilidade em comandos SQL no SQLite."""

    def __init__(self, banco_de_dados: ConexaoBancoDeDados):
        self._conexao = banco_de_dados.conexao

    def inserir(self, vulnerabilidade: Vulnerabilidade) -> Vulnerabilidade:
        """Insere uma nova vulnerabilidade e preenche o 'id' gerado pelo banco."""
        cursor = self._conexao.execute(
            """
            INSERT INTO vulnerabilidades (ativo_id, descricao, categoria, severidade, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                vulnerabilidade.ativo_id,
                vulnerabilidade.descricao,
                vulnerabilidade.categoria,
                vulnerabilidade.severidade.name,
                vulnerabilidade.status.name,
            ),
        )
        self._conexao.commit()
        vulnerabilidade.id = cursor.lastrowid
        return vulnerabilidade

    def atualizar(self, vulnerabilidade: Vulnerabilidade) -> None:
        """Grava as alterações de uma vulnerabilidade já existente."""
        self._conexao.execute(
            """
            UPDATE vulnerabilidades
            SET descricao = ?, categoria = ?, severidade = ?, status = ?
            WHERE id = ?
            """,
            (
                vulnerabilidade.descricao,
                vulnerabilidade.categoria,
                vulnerabilidade.severidade.name,
                vulnerabilidade.status.name,
                vulnerabilidade.id,
            ),
        )
        self._conexao.commit()

    def excluir(self, vulnerabilidade_id: int) -> None:
        self._conexao.execute("DELETE FROM vulnerabilidades WHERE id = ?", (vulnerabilidade_id,))
        self._conexao.commit()

    def buscar_por_id(self, vulnerabilidade_id: int) -> Optional[Vulnerabilidade]:
        linha = self._conexao.execute(
            "SELECT * FROM vulnerabilidades WHERE id = ?", (vulnerabilidade_id,)
        ).fetchone()
        return self._converter_linha_em_vulnerabilidade(linha) if linha else None

    def listar_por_ativo(self, ativo_id: int) -> List[Vulnerabilidade]:
        linhas = self._conexao.execute(
            "SELECT * FROM vulnerabilidades WHERE ativo_id = ? ORDER BY id", (ativo_id,)
        ).fetchall()
        return [self._converter_linha_em_vulnerabilidade(linha) for linha in linhas]

    def listar_todas(self) -> List[Vulnerabilidade]:
        linhas = self._conexao.execute("SELECT * FROM vulnerabilidades ORDER BY id").fetchall()
        return [self._converter_linha_em_vulnerabilidade(linha) for linha in linhas]

    @staticmethod
    def _converter_linha_em_vulnerabilidade(linha: sqlite3.Row) -> Vulnerabilidade:
        return Vulnerabilidade(
            id=linha["id"],
            ativo_id=linha["ativo_id"],
            descricao=linha["descricao"],
            categoria=linha["categoria"],
            severidade=Severidade[linha["severidade"]],
            status=StatusVulnerabilidade[linha["status"]],
        )
