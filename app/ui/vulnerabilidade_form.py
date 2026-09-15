"""Janela (formulário) usada para cadastrar ou editar uma vulnerabilidade."""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Optional

from app.exceptions import ErroDeValidacao
from app.models.enums import Severidade, StatusVulnerabilidade, rotulo_amigavel
from app.models.vulnerabilidade import Vulnerabilidade
from app.services.vulnerabilidade_service import VulnerabilidadeService


class JanelaFormularioVulnerabilidade(tk.Toplevel):
    """Formulário para cadastro ou edição de uma vulnerabilidade de um ativo.

    Quando 'vulnerabilidade_para_editar' é None, o formulário cadastra uma
    vulnerabilidade nova para o ativo indicado por 'ativo_id'. Caso
    contrário, edita a vulnerabilidade recebida.
    """

    def __init__(
        self,
        janela_pai: tk.Widget,
        servico_de_vulnerabilidades: VulnerabilidadeService,
        ativo_id: int,
        ao_salvar_com_sucesso: Callable[[], None],
        vulnerabilidade_para_editar: Optional[Vulnerabilidade] = None,
    ):
        super().__init__(janela_pai)
        self._servico_de_vulnerabilidades = servico_de_vulnerabilidades
        self._ativo_id = ativo_id
        self._ao_salvar_com_sucesso = ao_salvar_com_sucesso
        self._vulnerabilidade_para_editar = vulnerabilidade_para_editar

        self._rotulos_por_severidade = {
            rotulo_amigavel(severidade.name): severidade for severidade in Severidade
        }
        self._rotulos_por_status = {
            rotulo_amigavel(status.name): status for status in StatusVulnerabilidade
        }

        self.title("Editar Vulnerabilidade" if vulnerabilidade_para_editar else "Nova Vulnerabilidade")
        self.resizable(False, False)
        self.transient(janela_pai)

        self._construir_widgets()
        self._preencher_campos_se_estiver_editando()

        self.grab_set()
        self.focus_set()

    def _construir_widgets(self) -> None:
        quadro = ttk.Frame(self, padding=15)
        quadro.grid(row=0, column=0, sticky="nsew")

        ttk.Label(quadro, text="Descrição:").grid(row=0, column=0, sticky="w", pady=4)
        self._campo_descricao = ttk.Entry(quadro, width=40)
        self._campo_descricao.grid(row=0, column=1, pady=4)

        ttk.Label(quadro, text="Categoria:").grid(row=1, column=0, sticky="w", pady=4)
        self._campo_categoria = ttk.Entry(quadro, width=40)
        self._campo_categoria.grid(row=1, column=1, pady=4)

        ttk.Label(quadro, text="Severidade:").grid(row=2, column=0, sticky="w", pady=4)
        self._campo_severidade = ttk.Combobox(
            quadro, values=list(self._rotulos_por_severidade.keys()), state="readonly", width=38
        )
        self._campo_severidade.grid(row=2, column=1, pady=4)

        ttk.Label(quadro, text="Status:").grid(row=3, column=0, sticky="w", pady=4)
        self._campo_status = ttk.Combobox(
            quadro, values=list(self._rotulos_por_status.keys()), state="readonly", width=38
        )
        self._campo_status.grid(row=3, column=1, pady=4)

        quadro_de_botoes = ttk.Frame(quadro)
        quadro_de_botoes.grid(row=4, column=0, columnspan=2, pady=(15, 0))
        ttk.Button(quadro_de_botoes, text="Salvar", command=self._salvar).grid(
            row=0, column=0, padx=5
        )
        ttk.Button(quadro_de_botoes, text="Cancelar", command=self.destroy).grid(
            row=0, column=1, padx=5
        )

    def _preencher_campos_se_estiver_editando(self) -> None:
        if self._vulnerabilidade_para_editar is None:
            self._campo_severidade.current(0)
            self._campo_status.current(0)
            return

        vulnerabilidade = self._vulnerabilidade_para_editar
        self._campo_descricao.insert(0, vulnerabilidade.descricao)
        self._campo_categoria.insert(0, vulnerabilidade.categoria)
        self._campo_severidade.set(rotulo_amigavel(vulnerabilidade.severidade.name))
        self._campo_status.set(rotulo_amigavel(vulnerabilidade.status.name))

    def _salvar(self) -> None:
        severidade_selecionada = self._rotulos_por_severidade.get(self._campo_severidade.get())
        status_selecionado = self._rotulos_por_status.get(self._campo_status.get())

        try:
            if self._vulnerabilidade_para_editar is None:
                self._servico_de_vulnerabilidades.cadastrar(
                    ativo_id=self._ativo_id,
                    descricao=self._campo_descricao.get(),
                    categoria=self._campo_categoria.get(),
                    severidade=severidade_selecionada,
                    status=status_selecionado,
                )
            else:
                self._servico_de_vulnerabilidades.atualizar(
                    vulnerabilidade_id=self._vulnerabilidade_para_editar.id,
                    descricao=self._campo_descricao.get(),
                    categoria=self._campo_categoria.get(),
                    severidade=severidade_selecionada,
                    status=status_selecionado,
                )
        except ErroDeValidacao as erro:
            messagebox.showerror("Dados inválidos", str(erro), parent=self)
            return

        self._ao_salvar_com_sucesso()
        self.destroy()
