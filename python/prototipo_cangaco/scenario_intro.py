from ui import print_header, wait_for_enter
from save_manager import save_player_data


def intro_scene(player):
    print_header()
    print('Nordeste, final do século XIX — terras secas, sertões e histórias de coragem.')
    wait_for_enter()

    # Se nome não estiver definido, pergunta ao jogador
    if not player.get('name'):
        print('Qual o seu nome?')
        player_name = input('\nNome: ').strip()
        while player_name == '':
            player_name = input('Digite um nome válido: ').strip()
        player['name'] = player_name

    # Se ambição não estiver definida, pergunta qual o sonho
    if not player.get('ambition'):
        print('\nSeu maior sonho foi ser...')
        print('1 - Trabalhador e substituir seu pai nos trabalhos da família.')
        print('2 - Ir para as grandes cidades.')
        print('3 - Virar um artista.')
        choice = ''
        while choice not in ['1', '2', '3']:
            choice = input('\nEscolha (1/2/3): ').strip()
        if choice == '1':
            player['ambition'] = 'Trabalhador'
        elif choice == '2':
            player['ambition'] = 'Ir para as grandes cidades'
        else:
            player['ambition'] = 'Artista'

    wait_for_enter()
    print('Você morava com sua família numa casa simples no interior de Pernambuco.')
    wait_for_enter()

    print('Porém, próximo do seu aniversário de 15 anos, um grupo invade sua casa, mata seus pais e seus irmãos.')
    print('Apenas você sobrevive porque se escondeu.')
    wait_for_enter()

    print('Você caminha no sertão até que seu tio, grande amigo do seu pai, o encontra e o leva para casa.')
    print('Ele te cria. O tempo passa e, agora com 18 anos, enquanto limpava a casa seu tio diz que vai a Villa-Nova para comprar mantimentos.')
    print('Três dias se passam e ele não retorna. Você decide investigar. O jogo começa aqui.')
    wait_for_enter()

    # Se a ficha não existir, permite criar a ficha aqui
    if not player.get('stats'):
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
            print('Finalize a criação do personagem:')
            print(f'Pontos de Distribuição (PT): {remaining_points}\n')
            for stat_name in base_stats:
                print(f'Nível de {stat_name}: (Atual: {base_stats[stat_name]}, Máximo: {max_stat})')
            print('\nPara alocar pontos, digite um número inteiro. Digite 0 para pular.')

            for stat_name in base_stats:
                if remaining_points <= 0:
                    break
                current_value = base_stats[stat_name]
                max_add = max_stat - current_value
                if max_add <= 0:
                    continue
                prompt_text = f'\nQuanto deseja adicionar a {stat_name}? (0 a {min(max_add, remaining_points)}) '
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
                print(f'Ainda restam {remaining_points} pontos para distribuir.')
                choice = input('Deseja alocar os pontos restantes? (s/n) ').strip().lower()
                if choice in ['n', 'não', 'nao']:
                    break
                else:
                    continue
            else:
                break

        agility_level = base_stats.get('Agilidade', 1)
        action_points = 8 + agility_level * 2

        player['stats'] = base_stats
        player['action_points'] = action_points
        player['current_quest'] = 'Procurar tio em Villa-Nova'
        player['current_scene'] = 'intro'
        player['inventory'] = player.get('inventory', [])
        player['discovered_items'] = player.get('discovered_items', [])

        save_player_data(player)
        print('\nFicha criada e salva.')
        wait_for_enter()

    # Entrada na cena principal (cabana / exploração)
    while True:
        print_header()
        print('Você vê uma cabana... Sua casa que morava com o seu tio.')
        print('\n1) Entrar')
        print('2) Se afastar')
        print('3) Observar ao redor')
        choice = input('\nEscolha: ').strip()
        if choice == '1':
            enter_house(player)
            if all(x in player.get('discovered_items', []) for x in ['bau', 'prateleira', 'espingarda']):
                print('\nVocê já explorou tudo que precisava na casa.')
                wait_for_enter()
                player['current_scene'] = 'path'
                save_player_data(player)
                return player
        elif choice == '2':
            print('\nVocê tenta se afastar...')
            print('Você não pode ir agora, há coisas dentro da casa que precisam ser exploradas.')
            wait_for_enter()
        elif choice == '3':
            print('\nA cabana é pequena, com marcas de uso e pouca mobília. Há marcas na terra próximas à porta.')
            wait_for_enter()
        else:
            print('\nEntrada inválida.')
            wait_for_enter()


def enter_house(player):
    discovered = player.get('discovered_items', [])
    while True:
        print_header()
        perception_value = player.get('stats', {}).get('Percepção', 1)
        if perception_value < 4:
            print('[PER <4] Você entra na casa... Ela parece menor do que você se lembra, mas você sabe o caminho das coisas...')
        else:
            print('Você entra na casa. O ar está pesado, a memória mistura cheiro e poeira.')

        options = []
        if 'bau' in discovered:
            options.append(('1', 'Baú (Aberto)'))
        else:
            options.append(('1', 'Baú (Fechado)'))
        if 'prateleira' in discovered:
            options.append(('2', 'Prateleira (Vasculhada)'))
        else:
            options.append(('2', 'Prateleiras de Livros'))
        if 'espingarda' in discovered:
            options.append(('3', 'Espingarda (Coletada)'))
        else:
            options.append(('3', 'Espingarda na Parede'))

        all_done = all(x in discovered for x in ['bau', 'prateleira', 'espingarda'])
        if all_done:
            options.append(('4', 'Sair da casa'))

        print('\nVocê se depara com:')
        for key, text in options:
            print(f'{key}) {text}')

        choice = input('\nEscolha: ').strip()

        if choice == '1':
            if 'bau' in discovered:
                print('\nO baú já foi revirado.')
            else:
                print('\nVocê abre o baú e encontra: bolsa pequena, botas de couro, chapéu de couro')
                inventory = player.get('inventory', [])
                inventory.append('bolsa pequena')
                inventory.append('botas de couro')
                inventory.append('chapeu de couro')
                player['inventory'] = inventory
                discovered.append('bau')
                player['discovered_items'] = discovered
                save_player_data(player)
            wait_for_enter()
        elif choice == '2':
            if 'prateleira' in discovered:
                print('\nA prateleira já foi vasculhada.')
            else:
                print('\nVocê se depara com uma prateleira que deveria ter vários livros... Mas não há nada além de algumas miniaturas religiosas e uma bíblia surrada...')
                discovered.append('prateleira')
                player['discovered_items'] = discovered
                save_player_data(player)
            wait_for_enter()
        elif choice == '3':
            if 'espingarda' in discovered:
                print('\nA espingarda já está com você.')
            else:
                print('\nVocê retira a espingarda da parede e encontra alguns cartuchos junto com ela.')
                inventory = player.get('inventory', [])
                inventory.append('espingarda')
                inventory.append('cartuchos')
                player['inventory'] = inventory
                discovered.append('espingarda')
                player['discovered_items'] = discovered
                save_player_data(player)
            wait_for_enter()
        elif choice == '4' and all_done:
            print('\nVocê sai da casa depois de explorar tudo que precisava.')
            wait_for_enter()
            player['current_scene'] = 'path'
            save_player_data(player)
            return
        else:
            print('\nEntrada inválida.')
            wait_for_enter()
