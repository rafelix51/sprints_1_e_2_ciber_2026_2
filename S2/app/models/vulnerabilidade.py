"""Modelo que representa uma vulnerabilidade associada a um ativo de TI."""

from dataclasses import dataclass
from typing import Optional

from app.models.enums import Severidade, StatusVulnerabilidade


@dataclass
class Vulnerabilidade:
    """Representa uma vulnerabilidade encontrada em um ativo específico.

    O campo 'ativo_id' liga a vulnerabilidade ao ativo dono dela. O campo
    'id' só é preenchido depois que o registro é gravado no banco de dados.
    """

    ativo_id: int
    descricao: str
    categoria: str
    severidade: Severidade
    status: StatusVulnerabilidade
    id: Optional[int] = None
