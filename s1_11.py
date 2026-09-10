# Cria os sets
vulnerabilidades_ativo_1 = {"Senha fraca", "Software desatualizado", "Porta exposta"}
vulnerabilidades_ativo_2 = {"Senha fraca", "Falha de configuração", "Permissão inadequada"}

print(f"Vulnerabilidades do Ativo 1: {vulnerabilidades_ativo_1}")
print(f"Vulnerabilidades do Ativo 2: {vulnerabilidades_ativo_2}")

# Calculo da união dos dois sets
uniao = vulnerabilidades_ativo_1 | vulnerabilidades_ativo_2
print(f"\nUnião (todas as vulnerabilidades, sem repetir): {uniao}")

# Calculo da intersecao dos dois sets
intersecao = vulnerabilidades_ativo_1 & vulnerabilidades_ativo_2
print(f"Interseção (vulnerabilidades em comum): {intersecao}")


# Calculo do que tem exclusivamente em cada set
diferenca_simetrica = vulnerabilidades_ativo_1 ^ vulnerabilidades_ativo_2
print(f"Diferença simétrica (exclusivas de cada um): {diferenca_simetrica}")
