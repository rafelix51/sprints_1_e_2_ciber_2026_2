"""Modelo que representa um ativo de TI cadastrado no inventário."""

from dataclasses import dataclass
from typing import Optional

from app.models.enums import TipoAtivo


@dataclass
class Ativo:
    """Representa um ativo de TI (servidor, roteador, switch, etc.).

    O campo 'id' é opcional porque só é preenchido depois que o ativo é
    gravado no banco de dados (o SQLite gera o identificador único).
    """

    nome: str
    responsavel: str
    setor: str
    tipo: TipoAtivo
    descricao: str = ""
    id: Optional[int] = None
