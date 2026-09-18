"""Enumerações utilizadas para padronizar valores fixos da aplicação.

Usar Enum (em vez de strings soltas) evita erros de digitação e deixa
explícito, em um único lugar, quais são os valores válidos para cada campo.
"""

from enum import Enum


class TipoAtivo(Enum):
    """Tipos de ativos de TI que podem ser cadastrados no inventário."""

    SERVIDOR = 1
    ESTACAO_DE_TRABALHO = 2
    ROTEADOR = 3
    SWITCH = 4
    FIREWALL = 5
    IMPRESSORA = 6


class Severidade(Enum):
    """Nível de gravidade de uma vulnerabilidade."""

    BAIXA = 1
    MEDIA = 2
    ALTA = 3
    CRITICA = 4


class StatusVulnerabilidade(Enum):
    """Situação atual do tratamento de uma vulnerabilidade."""

    ABERTA = 1
    EM_TRATAMENTO = 2
    CORRIGIDA = 3
    ACEITA_COMO_RISCO = 4


def rotulo_amigavel(nome_do_enum: str) -> str:
    """Formata os nomes para exibição na tela (ex: 'EM_TRATAMENTO' vira 'Em Tratamento')."""
    return nome_do_enum.replace("_", " ").title()
