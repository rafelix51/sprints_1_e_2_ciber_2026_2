"""Testes da camada de regras de negócio (VulnerabilidadeService):
CRUD, validações e exclusão em cascata."""

from app.exceptions import ErroDeValidacao, VulnerabilidadeNaoEncontradaError
from app.models.enums import Severidade, StatusVulnerabilidade, TipoAtivo
from app.repositories.ativo_repository import AtivoRepository
from app.repositories.vulnerabilidade_repository import VulnerabilidadeRepository
from app.services.ativo_service import AtivoService
from app.services.vulnerabilidade_service import VulnerabilidadeService
from tests.base import CasoDeTesteComBancoTemporario

NOME_DO_LOGGER = "app.services.vulnerabilidade_service"


class TestVulnerabilidadeService(CasoDeTesteComBancoTemporario):
    def setUp(self) -> None:
        super().setUp()
        self.servico_de_ativos = AtivoService(AtivoRepository(self.banco))
        self.servico = VulnerabilidadeService(VulnerabilidadeRepository(self.banco))
        self.ativo = self.servico_de_ativos.cadastrar("Servidor-01", "Fulano", "TI", TipoAtivo.SERVIDOR)

    # --- Read (RF09: informar explicitamente quando não houver) -------

    def test_ativo_sem_vulnerabilidades_retorna_lista_vazia(self):
        self.assertEqual(self.servico.listar_por_ativo(self.ativo.id), [])

    def test_listar_por_ativo_retorna_apenas_vulnerabilidades_daquele_ativo(self):
        outro_ativo = self.servico_de_ativos.cadastrar("Servidor-02", "Fulano", "TI", TipoAtivo.SERVIDOR)
        self.servico.cadastrar(self.ativo.id, "Vuln A", "Rede", Severidade.BAIXA, StatusVulnerabilidade.ABERTA)
        self.servico.cadastrar(outro_ativo.id, "Vuln B", "Rede", Severidade.BAIXA, StatusVulnerabilidade.ABERTA)

        vulnerabilidades_do_primeiro_ativo = self.servico.listar_por_ativo(self.ativo.id)

        self.assertEqual(len(vulnerabilidades_do_primeiro_ativo), 1)
        self.assertEqual(vulnerabilidades_do_primeiro_ativo[0].descricao, "Vuln A")

    # --- Create -----------------------------------------------------

    def test_cadastrar_com_dados_validos_retorna_vulnerabilidade_persistida(self):
        with self.assertLogs(NOME_DO_LOGGER, level="INFO"):
            vulnerabilidade = self.servico.cadastrar(
                ativo_id=self.ativo.id,
                descricao="Senha fraca",
                categoria="Autenticação",
                severidade=Severidade.ALTA,
                status=StatusVulnerabilidade.ABERTA,
            )

        self.assertIsNotNone(vulnerabilidade.id)
        self.assertEqual(self.servico.listar_por_ativo(self.ativo.id), [vulnerabilidade])

    def test_cadastrar_com_descricao_vazia_levanta_erro_de_validacao(self):
        with self.assertRaises(ErroDeValidacao):
            self.servico.cadastrar(
                self.ativo.id, "", "Autenticação", Severidade.BAIXA, StatusVulnerabilidade.ABERTA
            )

    def test_cadastrar_com_categoria_vazia_levanta_erro_de_validacao(self):
        with self.assertRaises(ErroDeValidacao):
            self.servico.cadastrar(self.ativo.id, "Senha fraca", "", Severidade.BAIXA, StatusVulnerabilidade.ABERTA)

    def test_cadastrar_com_severidade_invalida_levanta_erro_de_validacao(self):
        with self.assertRaises(ErroDeValidacao):
            self.servico.cadastrar(self.ativo.id, "desc", "cat", "alta", StatusVulnerabilidade.ABERTA)

    def test_cadastrar_com_status_invalido_levanta_erro_de_validacao(self):
        with self.assertRaises(ErroDeValidacao):
            self.servico.cadastrar(self.ativo.id, "desc", "cat", Severidade.BAIXA, "aberta")

    # --- Update ---------------------------------------------------------

    def test_atualizar_altera_severidade_e_status(self):
        vulnerabilidade = self.servico.cadastrar(
            self.ativo.id, "Senha fraca", "Autenticação", Severidade.ALTA, StatusVulnerabilidade.ABERTA
        )

        with self.assertLogs(NOME_DO_LOGGER, level="INFO"):
            vulnerabilidade_atualizada = self.servico.atualizar(
                vulnerabilidade_id=vulnerabilidade.id,
                descricao="Senha fraca",
                categoria="Autenticação",
                severidade=Severidade.BAIXA,
                status=StatusVulnerabilidade.CORRIGIDA,
            )

        self.assertEqual(vulnerabilidade_atualizada.severidade, Severidade.BAIXA)
        self.assertEqual(vulnerabilidade_atualizada.status, StatusVulnerabilidade.CORRIGIDA)

    def test_atualizar_vulnerabilidade_inexistente_levanta_erro(self):
        with self.assertRaises(VulnerabilidadeNaoEncontradaError):
            self.servico.atualizar(999, "desc", "cat", Severidade.BAIXA, StatusVulnerabilidade.ABERTA)

    # --- Delete ---------------------------------------------------------

    def test_excluir_remove_vulnerabilidade_do_cache_e_do_banco(self):
        vulnerabilidade = self.servico.cadastrar(
            self.ativo.id, "Senha fraca", "Autenticação", Severidade.ALTA, StatusVulnerabilidade.ABERTA
        )

        with self.assertLogs(NOME_DO_LOGGER, level="INFO"):
            self.servico.excluir(vulnerabilidade.id)

        self.assertEqual(self.servico.listar_por_ativo(self.ativo.id), [])
        with self.assertRaises(VulnerabilidadeNaoEncontradaError):
            self.servico.excluir(vulnerabilidade.id)

    def test_excluir_vulnerabilidade_inexistente_levanta_erro(self):
        with self.assertRaises(VulnerabilidadeNaoEncontradaError):
            self.servico.excluir(999)

    # --- Exclusão em cascata (RF07) ------------------------------------

    def test_esquecer_vulnerabilidades_do_ativo_limpa_o_cache_apos_exclusao_do_ativo(self):
        self.servico.cadastrar(
            self.ativo.id, "Senha fraca", "Autenticação", Severidade.ALTA, StatusVulnerabilidade.ABERTA
        )

        self.servico_de_ativos.excluir(self.ativo.id)
        self.servico.esquecer_vulnerabilidades_do_ativo(self.ativo.id)

        self.assertEqual(self.servico.listar_por_ativo(self.ativo.id), [])
