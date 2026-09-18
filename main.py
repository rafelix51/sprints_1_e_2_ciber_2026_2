"""Ponto de entrada da aplicação de Inventário de Ativos de TI.

Este arquivo apenas monta as dependências (banco de dados, repositórios e
serviços) e inicia a interface gráfica. Toda a lógica da aplicação fica
organizada dentro do pacote 'app'.
"""

import logging

from app.logging_config import configurar_logging
from app.repositories.ativo_repository import AtivoRepository
from app.repositories.database import ConexaoBancoDeDados
from app.repositories.vulnerabilidade_repository import VulnerabilidadeRepository
from app.services.ativo_service import AtivoService
from app.services.vulnerabilidade_service import VulnerabilidadeService
from app.ui.main_window import JanelaPrincipal

logger = logging.getLogger(__name__)


def iniciar_aplicacao() -> None:
    configurar_logging()
    logger.info("Aplicação iniciada.")

    banco_de_dados = ConexaoBancoDeDados()

    servico_de_ativos = AtivoService(AtivoRepository(banco_de_dados))
    servico_de_vulnerabilidades = VulnerabilidadeService(VulnerabilidadeRepository(banco_de_dados))

    janela_principal = JanelaPrincipal(servico_de_ativos, servico_de_vulnerabilidades)
    janela_principal.mainloop()

    banco_de_dados.fechar()
    logger.info("Aplicação encerrada.")


if __name__ == "__main__":
    iniciar_aplicacao()
