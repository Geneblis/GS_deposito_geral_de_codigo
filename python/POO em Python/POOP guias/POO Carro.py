
#Self, refere-se à instância da classe atual, ou seja, um valor dela mesma.
# Self equivale this em outras linguagens
#  EX:
#   car1.modelo = "Mustang"
#   car1.ano = "1967"
#   car1.cor = "preto"
#   car1.para_vender = False
#
#  isto equivale a:  car1 = Carro("Mustang", 1967, "preto", False)
#
#
class Carro:
    def __init__(self, modelo, ano, cor, para_vender):
        self.modelo = modelo
        self.ano = ano
        self.cor = cor
        self.para_vender = para_vender

    def drive(self):
        print(f"voce dirige o {self.modelo}")

    def stop(self):
        print(f"voce parou o {self.modelo}")

    def descrever(self):
        print(f"Um {self.modelo} de cor {self.cor} do ano de {self.ano}.")

car1 = Carro("Mustang", 2024, "azul", False)
car2 = Carro("Covertte", 2020, "vermelho", True)

print(car1.modelo)
print(car2.modelo)

car1.drive()
car2.stop()

car1.descrever()
car2.descrever()