# Inventário de ativos

## Requisitos Funcionais (RF)

RF01 - O sistema deve exibir um menu/prompt com opções claras para todas as operações disponíveis (CRUD de ativos e vulnerabilidades).

RF02 - O sistema deve manter uma enumeração (Enum) com pelo menos 4 tipos de ativos de TI, cada um associado a um código inteiro.

RF03 - O sistema deve permitir cadastrar um novo ativo de TI com identificador único (inteiro), nome/hostname, responsável, setor/localização, tipo de ativo e lista inicial de vulnerabilidades (quando houver).

RF04 - O sistema deve gravar/persistir os dados dos ativos em arquivo(s) de texto, funcionando como base de dados da aplicação.

RF05 - O sistema deve permitir consultar/buscar um ativo pelo identificador único ou pelo nome/hostname, exibindo os dados de forma organizada.

RF06 - O sistema deve permitir atualizar dados de um ativo já cadastrado (responsável, setor, localização, tipo de ativo ou descrição).

RF07 - O sistema deve permitir excluir/remover um ativo da base de dados, removendo também as vulnerabilidades associadas a ele.

RF08 - O sistema deve permitir cadastrar vulnerabilidades associadas a um ativo, contendo descrição, categoria/tipo, severidade (baixa, média, alta, crítica) e status de tratamento (aberta, em tratamento, corrigida, aceita como risco).

RF09 - O sistema deve permitir visualizar as vulnerabilidades associadas a um ativo, informando explicitamente quando não houver vulnerabilidades registradas.

RF10 - O sistema deve utilizar estrutura de dicionário (dict/hash map) para indexar e otimizar buscas e consultas dos registros.

## Requisitos Não Funcionais (RNF)

RNF01 - O sistema deve ser implementado na linguagem Python.

RNF02 - O sistema deve realizar tratamento de erros e exceções para comandos inválidos, campos vazios ou tipos de dados incorretos.

RNF03 - A persistência dos dados deve ocorrer em arquivo(s) de texto, com gravação/concatenação estruturada.

RNF04 - O sistema deve utilizar estrutura de enumeração (Enum) para representar os tipos de ativos.

RNF05 - O sistema deve utilizar estrutura de dicionário (hash map) como mecanismo de otimização de desempenho nas buscas.

RNF06 - O código-fonte deve estar hospedado em repositório Git (GitHub, Bitbucket ou similar), com acesso disponível ao docente.

RNF07 - O desenvolvimento deve demonstrar uso de mais de 2 branches e realização de merge entre elas.

RNF08 - O sistema deve ser interativo e funcional mesmo com interface gráfica limitada (prompt/menu textual é aceitável).
