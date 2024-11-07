class Calculadora_classe:
    def __init__(self):
        self.operador = ""
        self.num1 = 0.0
        self.num2 = 0.0
        self.result = 0.0

    def definir_operador(self, operador):
        self.operador = operador

    def def_num1(self, num1):
        self.num1 = float(num1)

    def def_num2(self, num2):
        self.num2 = float(num2)

    def calcular(self):
        if self.operador == "+":
            self.result = self.num1 + self.num2
        elif self.operador == "-":
            self.result = self.num1 - self.num2
        elif self.operador == "*":
            self.result = self.num1 * self.num2
        elif self.operador == "/":
            self.result = self.num1 / self.num2
        else:
            print(f"{self.operador} é um comando invalido.")

    def get_result(self):
        return round(self.result, 3)

# Instância da Calculadora
calc = Calculadora_classe()

# Chamando as def
calc.definir_operador(input("Coloque uma operação (+ - * /) : "))
calc.def_num1(input("Coloque o primeiro numero: "))
calc.def_num2(input("Coloque o segundo numero: "))
calc.calcular()

print("Seu resultado foi:")
print(calc.get_result())