# Inventário de Ativos de TI

Repositório para armazenar os códigos do projeto das sprints 1 e 2 do curso de Cibersegurança da UFU 2026-2 

Aluno: Raphael Felix

Aplicação de cadastro (CRUD) de ativos de TI e de suas vulnerabilidades,
com interface gráfica em **Tkinter** e persistência em banco de dados
**SQLite**.

## Como executar

```bash
# (opcional) em distribuições Linux, garanta que o tkinter esteja instalado:
sudo apt install python3-tk

python3 main.py
```

Na primeira execução, o arquivo de banco de dados `data/inventario.db` é
criado automaticamente com as tabelas necessárias.

## Estrutura do projeto

```
main.py                       # Ponto de entrada da aplicação
requirements.txt
seed_dados_teste.py           # Script utilitário para popular o banco com dados fictícios
data/                         # Banco de dados SQLite (gerado em tempo de execução)
logs/                         # Log de auditoria (gerado em tempo de execução)
tests/                        # Testes automatizados (unittest) do CRUD de ativos e vulnerabilidades
app/
├── exceptions.py             # Exceções personalizadas da aplicação
├── logging_config.py         # Configuração central do logging/auditoria
├── models/                   # Entidades e enumerações
│   ├── enums.py               # TipoAtivo, Severidade, StatusVulnerabilidade
│   ├── ativo.py               # Entidade Ativo
│   └── vulnerabilidade.py     # Entidade Vulnerabilidade
├── repositories/             # Acesso direto ao SQLite (SQL puro)
│   ├── database.py
│   ├── ativo_repository.py
│   └── vulnerabilidade_repository.py
├── services/                 # Regras de negócio, validações, cache em dicionário e logging
│   ├── ativo_service.py
│   └── vulnerabilidade_service.py
└── ui/                       # Janelas Tkinter
    ├── main_window.py
    ├── ativo_form.py
    ├── vulnerabilidade_window.py
    └── vulnerabilidade_form.py
```

## Arquitetura em camadas

- **models**: classes simples (`dataclass`) que representam os dados, sem
  nenhuma lógica de banco de dados ou de interface.
- **repositories**: única camada que conversa com o SQLite. Cada método
  corresponde a uma operação SQL (inserir, atualizar, excluir, buscar).
- **services**: aplicam as regras de negócio (campos obrigatórios, tipos
  válidos etc.) antes de chamar o repositório. Também mantêm em memória um
  **cache em dicionário** dos ativos e vulnerabilidades já carregados, para
  otimizar buscas repetidas sem precisar acessar o banco a cada consulta.
- **ui**: janelas Tkinter que apenas exibem dados e chamam os serviços;
  não têm nenhum comando SQL nem regra de negócio.

## Funcionalidades

- Cadastro, edição, exclusão e busca (por ID ou nome) de ativos de TI.
- Ao excluir um ativo, as vulnerabilidades associadas são removidas em
  cascata (garantido pelo próprio banco de dados, com `ON DELETE CASCADE`).
- Cadastro, edição e exclusão de vulnerabilidades vinculadas a um ativo.
- Mensagem explícita quando um ativo não possui nenhuma vulnerabilidade
  cadastrada.
- Tratamento de erros de validação (campos vazios, tipos inválidos) exibido
  na própria interface gráfica, sem travar a aplicação.

## Logging / Auditoria

Toda ação de cadastro, edição e exclusão de ativos e vulnerabilidades — além
de tentativas inválidas (campo obrigatório vazio, tipo/severidade/status
inválido, busca por um ID inexistente) — é registrada em
`logs/auditoria.log`, servindo como evidência verificável do que foi feito
no sistema e quando.

Formato de cada linha: `data/hora [NÍVEL] módulo: mensagem`. Exemplo:

```
2026-09-14 22:10:03,512 [INFO] app.services.ativo_service: Ativo cadastrado: id=1 nome='DB-Server-01' responsavel='Raphael' setor='TI' tipo=SERVIDOR
2026-09-14 22:10:15,201 [WARNING] app.services.ativo_service: Validação de ativo falhou: campo obrigatório 'nome' não foi informado.
2026-09-14 22:11:02,884 [INFO] app.services.ativo_service: Ativo excluído: id=1 nome='DB-Server-01' (vulnerabilidades associadas removidas em cascata)
```

A configuração fica centralizada em `app/logging_config.py`
(`configurar_logging()`), chamada uma única vez ao iniciar a aplicação
(`main.py`). Mensagens de nível `INFO` (ações concluídas) vão só para o
arquivo; mensagens de nível `WARNING` (tentativas inválidas) aparecem tanto
no arquivo quanto no console.

## Testes automatizados

O CRUD completo de ativos e vulnerabilidades é coberto por testes
automatizados com `unittest` (biblioteca padrão do Python, sem dependências
extras). Para rodar toda a suíte a partir da raiz do projeto:

```bash
python3 -m unittest discover -s tests -v
```

Estrutura dos testes:

```
tests/
├── base.py                          # Classe base: cria/destrói um SQLite temporário por teste
├── test_ativo_repository.py         # CRUD de ativos direto na camada SQLite
├── test_vulnerabilidade_repository.py  # CRUD de vulnerabilidades + exclusão em cascata (RF07)
├── test_ativo_service.py            # CRUD + validações (RNF02) + cache em dicionário (RF10/RNF05)
└── test_vulnerabilidade_service.py  # CRUD + validações + RF09 (lista vazia quando não há vulnerabilidades)
```

Cada teste usa um banco de dados SQLite próprio, criado em um diretório
temporário e descartado ao final — os testes nunca leem ou alteram o banco
real da aplicação (`data/inventario.db`). Os testes de cadastro, edição e
exclusão também verificam (com `assertLogs`) que a ação correspondente foi
registrada no log de auditoria.
