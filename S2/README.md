# Inventário de Ativos de TI (Sprint 2)

Aplicação de cadastro (CRUD) de ativos de TI e de suas vulnerabilidades,
com interface gráfica em **Tkinter** e persistência em banco de dados
**SQLite**.

## Como executar

```bash
# (opcional) em distribuições Linux, garanta que o tkinter esteja instalado:
sudo apt install python3-tk

cd S2
python3 main.py
```

Na primeira execução, o arquivo de banco de dados `data/inventario.db` é
criado automaticamente com as tabelas necessárias.

## Estrutura do projeto

```
S2/
├── main.py                     # Ponto de entrada da aplicação
├── requirements.txt
├── data/                       # Banco de dados SQLite (gerado em tempo de execução)
└── app/
    ├── exceptions.py           # Exceções personalizadas da aplicação
    ├── models/                 # Entidades e enumerações
    │   ├── enums.py             # TipoAtivo, Severidade, StatusVulnerabilidade
    │   ├── ativo.py             # Entidade Ativo
    │   └── vulnerabilidade.py   # Entidade Vulnerabilidade
    ├── repositories/           # Acesso direto ao SQLite (SQL puro)
    │   ├── database.py
    │   ├── ativo_repository.py
    │   └── vulnerabilidade_repository.py
    ├── services/               # Regras de negócio, validações e cache em dicionário
    │   ├── ativo_service.py
    │   └── vulnerabilidade_service.py
    └── ui/                     # Janelas Tkinter
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
