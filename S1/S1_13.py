from enum import Enum

class Severidade(Enum):
    BAIXA = 1
    MEDIA = 2
    ALTA = 3
    CRITICA = 4
 
  
class StatusAtivo(Enum):
    ATIVO = 1
    INATIVO = 2
    EM_MANUTENCAO = 3

print("Severidade:")
for a in Severidade:
    print(f"Nome: {a.name} - Valor: {a.value}")
print("Status:")
for a in StatusAtivo:
    print(f"Nome: {a.name} - Valor: {a.value}")