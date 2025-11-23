# FILE: scenario_path.py
# Cena: caminho até Villa-Nova — agora com emboscada automática e opção de abrir inventário.

from ui import print_header, wait_for_enter
from save_manager import save_player_data
from inventory import open_inventory
from combat import start_combat

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
            # Emboscada: em vez de diálogos sobre um viajante, surge um ataque
            print('\nNo caminho, algo muda: um homem surge das sombras com uma faca...')
            print('Um cangaceiro se aproxima e quer roubar suas coisas!')
            wait_for_enter()
            # dispara combate definido em enemies.json (chave: 'ambush_cangaceiro')
            player = start_combat(player, 'ambush_cangaceiro') or player
            # após o combate, se ainda vivo, segue para Villa-Nova
            if player.get('hp', 0) > 0:
                player['current_scene'] = 'villanova'
                save_player_data(player)
                wait_for_enter()
                return player
            else:
                # jogador foi derrotado ou morreu; salva e retorna ao menu/cena anterior
                save_player_data(player)
                wait_for_enter()
                return player

        elif choice == '2':
            print('\nVocê para e conversa com moradores locais, obtendo pistas que podem ser úteis mais adiante.')
            inventory = player.get('inventory', [])
            # evita duplicatas checando ids já presentes
            existing_ids = [it.get('id') if isinstance(it, dict) else str(it).lower() for it in inventory]
            if 'moeda antiga' not in existing_ids:
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
