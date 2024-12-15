# Self equivale this em outras linguagens
class Estudantes:
    classe_ano = 2024
    num_estudantes = 0
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
        Estudantes.num_estudantes += 1 #aumentar o valor de numero total de estudantes por 1.

estudante1 = Estudantes("Joao", 14)
estudante2 = Estudantes("Janio", 24)

print(estudante1.nome, estudante1.idade, estudante1.classe_ano)
print(estudante2.nome, estudante2.idade, estudante2.classe_ano)
print(f"Numero total de estudantes de {Estudantes.classe_ano} são: {Estudantes.num_estudantes}")