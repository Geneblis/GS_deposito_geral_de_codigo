# FILE: scenario_path.py
# (apenas o conteúdo do arquivo atualizado — inclui a opção de abrir inventário)

from ui import print_header, wait_for_enter
from save_manager import save_player_data
from inventory import open_inventory

def path_scene(player):
    while True:
        print_header()
        print('Você parte do vilarejo em direção a Villa-Nova. O caminho é seco e o sol castiga.')
        print('\nOpções:')
        print('1) Seguir para Villa-Nova')
        print('2) Parar para buscar informações na estrada')
        print('3) Abrir Inventário')
        print('4) Voltar')
        choice = input('\nEscolha: ').strip()
        if choice == '1':
            print('\nVocê segue direto, sem distrações.')
            player['current_scene'] = 'villanova'
            save_player_data(player)
            wait_for_enter()
            return player
        elif choice == '2':
            print('\nVocê para e conversa com moradores locais, obtendo pistas que podem ser úteis mais adiante.')
            inventory = player.get('inventory', [])
            if 'moeda antiga' not in [it.get('id') for it in inventory]:
                # adicionar item convertendo para formato normalizado
                inventory.append({
                    'id': 'moeda antiga',
                    'name': 'Moeda Antiga',
                    'qty': 1,
                    'weight': 0.05,
                    'effects': 'Relíquia',
                    'bonus_capacity': 0,
                    'equipable': False,
                    'equipped': False
                })
                player['inventory'] = inventory
            player['current_scene'] = 'villanova'
            save_player_data(player)
            wait_for_enter()
            return player
        elif choice == '3':
            open_inventory(player)
        elif choice == '4':
            return player
        else:
            print('\nEscolha inválida.')
            wait_for_enter()
