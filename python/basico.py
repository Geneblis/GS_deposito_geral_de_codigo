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
for i in range(0,2):
    for j in range(0,2):
        print(i, j)

#While loops são usados para executar blocos de código enquanto uma condição for verdadeira.
while x < 5:
    print(x) #Se print antes da soma, o resultado no terminal será o ultimo digito antes da funcao ter retornado falsa/concluida.
    x += 1

calculo_elevado_a = 3 ** 4 #3 elevado a 4
print(calculo_elevado_a)
resto_de_calculo = 3 % 4 #3 / 4 = x, x resultado eh o resto da operacao.
print(resto_de_calculo)

if x == 5:
    print(x, "é igual a cinco.")
elif x > 10:
    print("x é maior que 10")
else:
    print("x é menor ou igual a 10")


#Função com passagem de parâmetros e retorno
def soma(x, y):
    return x + y #retorno
print(soma(3, 5))  # Saída: 8

#Função com passagem de parâmetro, sem retorno
def greet(nome): #nome eh parametro
    print("Olá, " + nome + "!")
greet("João")  # Saída: Olá, João!


def energia_potencial(m, h, g=10):
    return m*g*h
valor = energia_potencial(10,10) #Colocou valores em m e h.
print(valor)

#range(start, stop, step)
#for i in range() é um valor exclusivo. O ultimo digito não é printado ao ser atingindo. 
print(list(range(1,10,2)))
print(list(range(10)))

def kagadas(idk):
    idk = None
    idk = str(input("Coloque um valor para idk \n"))
    print(idk)

kagadas("sla")

"""    
Aqui, self é um atributo da instância da classe.
Você usa self para garantir que ele seja acessível em qualquer outro método da classe.
Se você não usasse self, o Python acharia que a variável é apenas local dentro do método e não poderia ser acessada em outros métodos.
"""
class Basico:
    def __init__(self):
        pass  
    def _naoSei(sla):
        print(sla)

basicly = Basico()
basicly._naoSei("ops!")