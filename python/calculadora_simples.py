operador = input("Coloque uma operação (+ - * /) : ")
num1 = float(input("Coloque o primeiro numero: "))
num2 = float(input("Coloque o segundo numero: "))


if operador == "+":
    result = num1 + num2
    print("Seu resultado foi:")
    print(round(result, 3))
elif operador == "-":
    result = num1 - num2
    print("Seu resultado foi:")
    print(round(result, 3))
elif operador == "*":
    result = num1 * num2
    print("Seu resultado foi:")
    print(round(result, 3))
elif operador == "/":
    result = num1 / num2
    print("Seu resultado foi:")
    print(round(result, 3))

else: 
    print(f"{operador} é um comando invalido.")