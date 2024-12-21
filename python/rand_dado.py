import random

escolha_dado = 0

while escolha_dado == 0:
    escolha_dado = int(input("Qual tipo de dado você quer rodar? \n\n1- Dois(2x) dados de 6 lados\n2- Um (1x) dado de 20 lados\n"))

while escolha_dado in [1, 2]:
    if escolha_dado == 1:
        escolha = input("Rodar o dado? (s/n): ").lower()
        if escolha == "s":
            dado1 = random.randint(1, 6)
            dado2 = random.randint(1, 6)
            print(f'({dado1}, {dado2})')
        elif escolha == "n":
            print("Obrigado por jogar!")
            break
        else:
            print("Escolha inválida!")
    
    elif escolha_dado == 2:
        escolha = input("Rodar o dado? (s/n): ").lower()
        if escolha == "s":
            dado1 = random.randint(1, 20)
            print(f'({dado1})')
        elif escolha == "n":
            print("Obrigado por jogar!")
            break
        else:
            print("Escolha inválida!")