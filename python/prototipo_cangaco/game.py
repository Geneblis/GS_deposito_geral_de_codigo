import sys
from ui import print_header, wait_for_enter
from save_manager import load_saves, save_player_data, SAVE_FILE
import scenario_intro
import scenario_path
import scenario_villanova


def main_menu():
    while True:
        print_header()
        print('1) Jogar - Novo Jogo')
        print('2) Jogar - Jogo já Existente')
        print('3) Sair')
        choice = input('Escolha: ').strip()
        if choice == '1' or choice.lower() in ['jogar', 'novo']:
            start_new_game()
        elif choice == '2' or choice.lower() in ['carregar', 'load', 'existente']:
            load_game()
        elif choice == '3' or choice.lower() == 'sair':
            print('Até mais.')
            sys.exit(0)
        else:
            print('Opção inválida. Tente novamente.')
            wait_for_enter()


def start_new_game():
    print_header()
    print('Iniciando novo jogo...')
    wait_for_enter()

    character = {
        'name': '',
        'ambition': '',
        'stats': None,
        'action_points': None,
        'current_quest': 'Procurar tio em Villa-Nova',
        'current_scene': 'intro',
        'inventory': [],
        'discovered_items': []
    }

    save_player_data(character)

    character = scenario_intro.intro_scene(character)
    if character.get('current_scene') == 'path':
        character = scenario_path.path_scene(character)
    if character.get('current_scene') == 'villanova':
        character = scenario_villanova.villanova_scene(character)

    return


def create_character(player_name, ambition_text):
    base_stats = {
        'Força': 1,
        'Agilidade': 1,
        'Percepção': 1,
        'Técnica': 1,
        'Presença': 1
    }
    remaining_points = 11
    max_stat = 10

    while True:
        print_header()
        print('Distribua seus pontos (PT: {0})'.format(remaining_points))
        for stat_name in base_stats:
            current_value = base_stats[stat_name]
            print("{0}: (Atual: {1}, Máximo: {2})".format(stat_name, current_value, max_stat))
        print('Para alocar pontos, digite um número inteiro. Digite 0 para pular.')

        for stat_name in base_stats:
            if remaining_points <= 0:
                break
            current_value = base_stats[stat_name]
            max_add = max_stat - current_value
            if max_add <= 0:
                continue
            prompt_text = 'Quanto deseja adicionar a {0}? (0 a {1}) '.format(stat_name, min(max_add, remaining_points))
            valid_input = False
            while not valid_input:
                entry = input(prompt_text).strip()
                try:
                    add_points = int(entry)
                    if add_points < 0:
                        print('Número negativo não é permitido.')
                        continue
                    if add_points > remaining_points:
                        print('Você não tem pontos suficientes.')
                        continue
                    if add_points > max_add:
                        print('Excede o máximo permitido para esta habilidade.')
                        continue
                    base_stats[stat_name] = current_value + add_points
                    remaining_points = remaining_points - add_points
                    valid_input = True
                except ValueError:
                    print('Entrada inválida. Digite um número inteiro.')
        if remaining_points > 0:
            print_header()
            print('Ainda restam {0} pontos para distribuir.'.format(remaining_points))
            choice = input('Deseja alocar os pontos restantes? (s/n) ').strip().lower()
            if choice == 'n' or choice == 'não' or choice == 'nao':
                break
            else:
                continue
        else:
            break

    agility_level = base_stats.get('Agilidade', 1)
    action_points = 8 + agility_level * 2

    character_sheet = {
        'name': player_name,
        'ambition': ambition_text,
        'stats': base_stats,
        'action_points': action_points,
        'current_quest': 'Procurar tio em Villa-Nova',
        'current_scene': 'intro',
        'inventory': [],
        'discovered_items': []
    }
    return character_sheet


def load_game():
    players = load_saves()
    if not players:
        print('Nenhum save encontrado.')
        wait_for_enter()
        return
    print_header()
    print('Saves encontrados:')
    for idx in range(len(players)):
        print('{0}) {1}'.format(idx + 1, players[idx].get('name', 'sem-nome')))
    choice = ''
    while True:
        choice = input('Escolha um save pelo número (ou 0 para voltar): ').strip()
        try:
            num = int(choice)
            if num == 0:
                return
            if 1 <= num <= len(players):
                player_data = players[num - 1]
                print('Carregando {0}...'.format(player_data.get('name')))
                wait_for_enter()
                resume_scene(player_data)
                return
        except ValueError:
            pass
        print('Entrada inválida.')


def resume_scene(player):
    scene = player.get('current_scene', 'intro')
    if scene == 'intro':
        player = scenario_intro.intro_scene(player)
    if player.get('current_scene') == 'path':
        player = scenario_path.path_scene(player)
    if player.get('current_scene') == 'villanova':
        player = scenario_villanova.villanova_scene(player)
    return
