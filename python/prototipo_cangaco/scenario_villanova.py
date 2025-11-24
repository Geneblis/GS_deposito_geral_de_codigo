# FILE: scenario_villanova.py
# (atualizado para incluir opção de abrir inventário)

from ui import print_header, wait_for_enter
from save_manager import save_player_data
from inventory import open_inventory

def villanova_scene(player):
    while True:
        print_header()
        print('Villa-Nova — o vilarejo parece agitado. Pessoas cochicham e olham para os visitantes.')
        print('\nOpções:')
        print('1) Investigar o desaparecimento do seu tio')
        print('2) Conversar com os moradores')
        print('3) Abrir Inventário')
        print('4) Voltar')
        choice = input('\nEscolha: ').strip()
        if choice == '1':
            print('\nVocê começa a investigar....')
            print("\n\n\n")
            print("Esse é o final do prototipo, ate aqui voce viu um basico da narrativa, gerenciamento de inventario e uma ideia muito basica do combate final.")
            player['current_scene'] = 'villanova_exploring'
            save_player_data(player)
            wait_for_enter()
            return player
        elif choice == '2':
            print('\nMoradores dão pistas, alguns parecem desconfiados.')
            wait_for_enter()
        elif choice == '3':
            open_inventory(player)
        elif choice == '4':
            return player
        else:
            print('\nEntrada inválida.')
            wait_for_enter()
