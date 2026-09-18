# Especificação Consolidada — Sistema de Inventário de Ativos e Vulnerabilidades
**Versão:** 1.0

Este documento consolida requisitos, modelo de dados, regras de entrada/saída, critérios de aceitação e rastreabilidade em uma única fonte de verdade para implementação, revisão e teste.

---

## 1. Escopo

### 1.1 Dentro do escopo
- CRUD completo de ativos de TI (criar, consultar, atualizar, remover).
- Cadastro e visualização de vulnerabilidades associadas a um ativo (sem CRUD completo de vulnerabilidade — não há requisito de remoção ou busca isolada de vulnerabilidade fora do contexto do ativo).
- Persistência simples.
- Interface via prompt/menu textual (interface gráfica não é exigida).
- Uso de Enum (tipos de ativo) e dict (indexação/busca) como estruturas de dados obrigatórias.
- Controle de versão em Git, com uso de múltiplas branches e merge.

### 1.2 Fora de escopo
- Autenticação, autorização ou controle de múltiplos usuários simultâneos.
- Integração com bases de vulnerabilidades reais (CVE, NVD etc.) — vulnerabilidades são cadastradas manualmente (conforme enunciado).
- Relatórios, dashboards ou exportação de dados (ex.: CSV, PDF).

---

## 2. Modelo de Dados

### 2.1 Entidade: Ativo

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| `id_ativo` | inteiro | Sim | Único no sistema (chave do dicionário de ativos) |
| `nome_hostname` | texto | Sim | Não pode ser vazio |
| `responsavel` | texto | Sim | Não pode ser vazio |
| `setor_localizacao` | texto | Sim | Não pode ser vazio |
| `tipo_ativo` | Enum (`TipoAtivo`) | Sim | Deve pertencer aos valores definidos no Enum (RF02) |
| `vulnerabilidades` | lista/dict de Vulnerabilidade | Não | Pode ser vazia; inicial no cadastro (RF03) ou incluída depois (RF08) |

### 2.2 Entidade: Vulnerabilidade (associada a um ativo)

| Campo | Tipo | Obrigatório | Observação |
|---|---|---|---|
| `descricao` | texto | Sim | Não pode ser vazio |
| `categoria` | texto | Sim | Não pode ser vazio |
| `severidade` | Enum (`Severidade`) | Sim | baixa / média / alta / crítica |
| `status` | Enum (`StatusVulnerabilidade`) | Sim | aberta / em tratamento / corrigida / aceita como risco |

---

## 3. Requisitos de Entrada e Saída (E/S)

| Requisito | Entrada esperada | Saída esperada |
|---|---|---|
| RF01 | Opção numérica do menu | Menu textual com todas as operações listadas, ou mensagem de erro se a opção for inválida |
| RF02 | — (consulta interna) | Lista de tipos de ativo com nome e código inteiro |
| RF03 | id_ativo, nome_hostname, responsavel, setor_localizacao, tipo_ativo, vulnerabilidades iniciais (opcional) | Confirmação de cadastro **ou** mensagem de erro específica (ID duplicado, campo vazio, tipo inválido) |
| RF04 | Dados do ativo já validados | Registro gravado em arquivo de texto, recuperável em nova execução |
| RF05 | id_ativo **ou** nome_hostname | Dados completos do ativo formatados, ou mensagem "não encontrado" |
| RF06 | id_ativo do ativo-alvo + novo(s) valor(es) do campo a atualizar | Confirmação com dado atualizado, ou erro (ativo inexistente / valor inválido) |
| RF07 | id_ativo do ativo-alvo | Confirmação de remoção (ativo e vulnerabilidades associadas), ou erro (ativo inexistente) |
| RF08 | id_ativo do ativo-alvo + descricao, categoria, severidade, status da vulnerabilidade | Confirmação de cadastro, ou erro (ativo inexistente / campo vazio / severidade ou status fora da escala) |
| RF09 | id_ativo do ativo-alvo | Lista de vulnerabilidades (descrição, severidade, status) **ou** mensagem explícita de ausência de vulnerabilidades |
| RF10 | — (estrutural) | Buscas por `id_ativo` resolvidas via acesso direto a `dict[chave]`, não por varredura sequencial |

---

## 4. Regras de Tratamento de Entradas e Saídas

**Regras gerais (RNF02):**
- **R1:** nenhuma entrada vazia ou só com espaços é aceita em campo obrigatório — validar com `.strip()` antes de gravar.
- **R2:** entradas numéricas (ex.: `id_ativo`) devem ser validadas com verificação de tipo (`str.isdigit()` ou `try/except ValueError`) antes da conversão.
- **R3:** nenhuma exceção não tratada pode encerrar o programa; toda operação de entrada deve estar protegida por validação ou `try/except`.
- **R4:** valores de Enum (tipo de ativo, severidade, status) só são aceitos se pertencerem aos valores predefinidos; qualquer outro valor gera mensagem de erro e nova solicitação, sem gravar dado inconsistente.
- **R5:** o `id_ativo` é imutável após o cadastro (não é atualizável via RF06 — apenas responsável, setor, localização, tipo ou descrição).

**Regras específicas de saída:**
- **R6:** toda saída de dados de um ativo (RF05, RF09) deve ser formatada de forma legível (rótulos + valores alinhados), nunca a impressão bruta de uma estrutura interna (ex.: `dict` cru).
- **R7:** a ausência de resultado (ativo não encontrado, sem vulnerabilidades) deve gerar mensagem textual explícita — nunca uma saída vazia silenciosa.
- **R8:** mensagens de erro devem indicar **qual** campo ou condição falhou, não apenas "erro genérico".

**Regras de persistência (RF04/RNF03):**
- **R9:** cada gravação em arquivo deve preservar os registros já existentes (concatenação/reescrita controlada), nunca sobrescrever a base inteira de forma destrutiva por engano.
- **R10:** ao remover um ativo (RF07), suas vulnerabilidades associadas devem ser removidas do mesmo registro/arquivo, mantendo a consistência da base.

---

## 5. Critérios de Aceitação por Requisito

Nenhum requisito fica sem critério de aceitação — cada linha abaixo é testável e observável.

| Requisito | Critério(s) de Aceitação |
|---|---|
| RF01 | CA: menu exibe todas as operações disponíveis; opção inválida não encerra o programa e reexibe o menu. |
| RF02 | CA: existem ≥ 4 tipos de ativo, cada um com código inteiro único, acessíveis via Enum. |
| RF03 | CA1: cadastro com dados válidos persiste o ativo e é localizável depois. CA2: ID duplicado é rejeitado. CA3: campo obrigatório vazio é rejeitado. CA4: tipo fora do Enum é rejeitado. |
| RF04 | CA: dados gravados em uma execução são recuperáveis integralmente após reiniciar o programa. |
| RF05 | CA1: busca por ID retorna o ativo correto. CA2: busca por nome/hostname retorna o ativo correto. CA3: busca por ID/nome inexistente informa "não encontrado" sem erro não tratado. |
| RF06 | CA1: atualização de campo permitido reflete corretamente em consulta posterior. CA2: atualização de ativo inexistente é rejeitada. CA3: valor de tipo inválido é rejeitado, mantendo o valor anterior. |
| RF07 | CA1: remoção de ativo existente o torna não localizável, junto com suas vulnerabilidades. CA2: remoção de ativo inexistente é rejeitada sem alterar a base. |
| RF08 | CA1: vulnerabilidade com dados completos e válidos é associada ao ativo. CA2: cadastro para ativo inexistente é rejeitado. CA3: severidade/status fora da escala é rejeitado. |
| RF09 | CA1: vulnerabilidades existentes são exibidas com descrição, severidade e status. CA2: ausência de vulnerabilidades gera mensagem explícita (não lista vazia silenciosa). |
| RF10 | CA: inspeção de código confirma que ativos são indexados em `dict` e que buscas usam acesso direto por chave. |
| RNF02 | CA: nenhum teste de entrada inválida (campo vazio, tipo incorreto, comando inexistente) gera exceção não tratada ou encerra o programa. |
| RNF06/RNF07 | CA: repositório Git público/compartilhado com o docente contém histórico com ≥ 2 branches e ao menos um merge realizado. |

---

## 6. Rastreabilidade Completa

| Requisito | Critério(s) de Aceitação | Cenário(s) de Teste | Campos do modelo envolvidos |
|---|---|---|---|
| RF01 | CA (menu) | 1.1, 1.2 | — |
| RF02 | CA (enum tipos) | 2.1 | `tipo_ativo` |
| RF03 | CA1–CA4 | 3.1, 3.2 | `id_ativo`, `nome_hostname`, `responsavel`, `setor_localizacao`, `tipo_ativo` |
| RF04 | CA (persistência) | 4.1 | todos os campos de Ativo |
| RF05 | CA1–CA3 | 5.1, 5.2, 5.3 | `id_ativo`, `nome_hostname` |
| RF06 | CA1–CA3 | 6.1, 6.2 | `responsavel`, `setor_localizacao`, `tipo_ativo` |
| RF07 | CA1–CA2 | 7.1 | `id_ativo`, `vulnerabilidades` |
| RF08 | CA1–CA3 | 8.1, 8.2 | `descricao`, `categoria`, `severidade`, `status` |
| RF09 | CA1–CA2 | 9.1, 9.2 | `vulnerabilidades` |
| RF10 | CA (estrutural) | 10.1 | `id_ativo` (chave do dict) |
