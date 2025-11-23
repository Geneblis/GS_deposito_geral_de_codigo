# scenario_path.py

from ui import print_header, wait_for_enter
from save_manager import save_player_data
from inventory import open_inventory
from combat import start_combat

def path_scene(player):
    while True:
        print_header()
        print('Você parte da cabana em direção a Villa-Nova. O caminho é seco e o sol castiga.\n\n')
	print('Durante o caminho, você se depara com uma casa feita de barro, com os conhecimentos do seu tio, você sabe que a pequena casa pertence a Rodolfo, um pequeno agricultor.\n')
        print('\nOpções:')
        print('1) Seguir para Villa-Nova')
        print('2) Perguntar sobre o paradeiro seu Tio a Rodolfo')
        print('3) Abrir Inventário')
        print('4) Voltar ao Menu')
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
                save_player_data(player)
                wait_for_enter()
                return player

        elif choice == '2':
            print('\nVocê para e conversa com Rodolfo e alguns dos locais, obtendo pistas que podem ser úteis mais adiante.')
	    print('\nRodolfo da dicas de como chegar a Villa-Nova, e lhe oferece abrigo caso precise.'\n\n)
		#funcionalidade para desbloquear continuar o caminho para Villa Nova.
            wait_for_enter()

        elif choice == '3':
            open_inventory(player)

        elif choice == '4':
            return player

        else:
            print('\nEscolha inválida.')
            wait_for_enter()
