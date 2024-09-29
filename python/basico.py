##################################################### Definicao de Variaveis
x = 0
y = 2
z = 5
frutas = ["maçã", "banana", "laranja"]

#####################################################   Codigo
print(z > y and x < 10)  # Saída: True
print(z > y or x < 0)  # Saída: True

#User Input
z = int(input("Coloque um novo valor para Z \n"))
print(z > y and x < 10) 
print(z > y or x < 0) 

#For loops são usados para iterar sobre sequências.
for fruta in frutas:
    print(fruta)

#While loops são usados para executar blocos de código enquanto uma condição for verdadeira.
while x < 5:
    print(x) #Se print antes da soma, o resultado no terminal será o ultimo digito antes da funcao ter retornado falsa/concluida.
    x += 1

if x == 5:
    print(x, "é igual a cinco.")
elif x > 10:
    print("x é maior que 10")
else:
    print("x é menor ou igual a 10")


def soma(x, y):
    return x + y
print(soma(3, 5))  # Saída: 8

def greet(nome):
    print("Olá, " + nome + "!")
greet("João")  # Saída: Olá, João!

def eh_inteiro(valor):
    #verifica se um valor eh inteiro
    return isinstance(valor, int)

###########         Nota:
#                       Essa foi de longe, a linguagem mais fulera que tive os desprazer de decorar.
#                                                                                                  -G