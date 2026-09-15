# Critérios de Aceitação e Casos de Teste
**Card:** Critérios de Aceitação | **Tema:** Validação de funcionalidades do Trabalho 1

## 1. Critérios de Aceitação — Cadastro de Ativo

Uma funcionalidade de cadastro de ativo é considerada **pronta** (Definition of Done) quando:

- **CA1:** o sistema exige e valida ID (inteiro), nome/hostname, responsável, setor/localização e tipo de ativo antes de gravar o registro.
- **CA2:** o sistema rejeita o cadastro se o ID informado já existir na base, exibindo mensagem de erro clara.
- **CA3:** o sistema rejeita entradas com campos obrigatórios vazios ou de tipo incorreto (ex.: texto no lugar do ID numérico), sem encerrar o programa.
- **CA4:** o tipo de ativo informado deve pertencer à enumeração pré-definida (NOTEBOOK, SERVIDOR, ROTEADOR, etc.); tipos fora da lista são recusados.
- **CA5:** após o cadastro bem-sucedido, o ativo passa a estar disponível para consulta, atualização e remoção.

## 2. Critérios de Aceitação — Cadastro de Vulnerabilidade

- **CA1:** o sistema só permite cadastrar vulnerabilidade para um ativo que já exista na base.
- **CA2:** o sistema exige descrição, categoria, severidade e status de tratamento; nenhum desses campos pode ficar vazio.
- **CA3:** a severidade só aceita valores válidos da escala (baixa, média, alta, crítica); valores fora da escala são rejeitados.
- **CA4:** o status só aceita valores válidos (aberta, em tratamento, corrigida, aceita como risco).
- **CA5:** após o cadastro, a vulnerabilidade aparece corretamente associada ao ativo em consultas futuras.

## 3. Casos de Teste

**Caso de Teste 1 — Cadastro de ativo com ID duplicado**
- **Entrada:** cadastrar ativo com ID = 1 (já existente).
- **Resultado esperado:** o sistema recusa o cadastro e exibe mensagem informando que o ID já está em uso, sem alterar o registro original.

**Caso de Teste 2 — Consulta de ativo sem vulnerabilidades**
- **Entrada:** consultar vulnerabilidades de um ativo cadastrado que nunca recebeu nenhuma vulnerabilidade.
- **Resultado esperado:** o sistema exibe a mensagem "ativo sem vulnerabilidades registradas", sem erros ou listas vazias mal formatadas.