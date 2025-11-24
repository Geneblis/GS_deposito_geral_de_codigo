# FILE: scenario_path.py
# Cena: caminho até Villa-Nova com encontro social (Rodolfo) que reage a checks de atributos.
from ui import print_header, wait_for_enter
from save_manager import save_player_data
from inventory import open_inventory, ITEM_CATALOG
from combat import start_combat
import random

def _make_item_from_catalog(key, qty=1):
    key = key.lower()
    cat = ITEM_CATALOG.get(key, None)
    if not cat:
        return {
            'id': key,
            'name': key.title(),
            'qty': qty,
            'weight': 1.0,
            'effects': '',
            'bonus_capacity': 0,
            'equipable': False,
            'equipped': False,
            'slot': None,
            'damage_min': 0,
            'damage_max': 0,
            'ap_cost': 0,
            'range': 0,
            'ammo_type': None,
            'ammo_per_shot': 0,
            'armor_hp': 0
        }
    return {
        'id': key,
        'name': cat.get('display', key.title()),
        'qty': qty,
        'weight': float(cat.get('weight', 1.0)),
        'effects': cat.get('effects', ''),
        'bonus_capacity': int(cat.get('bonus_capacity', 0)),
        'equipable': bool(cat.get('equipable', False)),
        'equipped': False,
        'slot': cat.get('slot') if 'slot' in cat else None,
        'damage_min': int(cat.get('damage_min', 0)),
        'damage_max': int(cat.get('damage_max', 0)),
        'ap_cost': int(cat.get('ap_cost', 0)),
        'range': int(cat.get('range', 0)),
        'ammo_type': cat.get('ammo_type'),
        'ammo_per_shot': int(cat.get('ammo_per_shot', 0)),
        'armor_hp': int(cat.get('armor_hp', 0))
    }

def _ensure_inventory_normalized(player):
    inv = player.get('inventory', [])
    if not inv:
        player['inventory'] = []
        return
    normalized = []
    changed = False
    for it in inv:
        if isinstance(it, str):
            changed = True
            normalized.append(_make_item_from_catalog(it, qty=1))
        elif isinstance(it, dict):
            item = dict(it)
            item.setdefault('id', item.get('name', '').lower())
            item.setdefault('qty', int(item.get('qty', 1)))
            item.setdefault('weight', float(item.get('weight', 1.0)))
            item.setdefault('effects', item.get('effects', ''))
            item.setdefault('bonus_capacity', int(item.get('bonus_capacity', 0)))
            item.setdefault('equipable', bool(item.get('equipable', False)))
            item.setdefault('equipped', bool(item.get('equipped', False)))
            item.setdefault('slot', item.get('slot', None))
            item.setdefault('damage_min', int(item.get('damage_min', 0)))
            item.setdefault('damage_max', int(item.get('damage_max', 0)))
            item.setdefault('ap_cost', int(item.get('ap_cost', 0)))
            item.setdefault('range', int(item.get('range', 0)))
            item.setdefault('ammo_type', item.get('ammo_type', None))
            item.setdefault('ammo_per_shot', int(item.get('ammo_per_shot', 0)))
            item.setdefault('armor_hp', int(item.get('armor_hp', 0)))
            normalized.append(item)
        else:
            changed = True
            normalized.append(_make_item_from_catalog(str(it), qty=1))
    if changed:
        player['inventory'] = normalized
        save_player_data(player)

def _add_item_to_player(player, item_key, qty=1):
    _ensure_inventory_normalized(player)
    inv = player.get('inventory', [])
    item_key = item_key.lower()
    for it in inv:
        if isinstance(it, dict) and it.get('id') == item_key:
            it['qty'] = int(it.get('qty', 1)) + qty
            player['inventory'] = inv
            save_player_data(player)
            return
    new_item = _make_item_from_catalog(item_key, qty=qty)
    inv.append(new_item)
    player['inventory'] = inv
    save_player_data(player)

def _player_has_item(player, item_key):
    _ensure_inventory_normalized(player)
    for it in player.get('inventory', []):
        if isinstance(it, dict) and it.get('id') == item_key and int(it.get('qty', 1)) > 0:
            return True
    return False

def _ensure_rodolfo_flags(player):
    if 'rodolfo_flags' not in player:
        player['rodolfo_flags'] = {
            'met': False,
            'gave_food': False,
            'gave_ammo': False,
            'gave_armor': False,
            'gave_kit': False
        }

def _presence_check(player, difficulty_base=30):
    presence = int(player.get('stats', {}).get('Presença', 1))
    chance = difficulty_base + presence * 10
    if chance > 95:
        chance = 95
    roll = random.randint(1, 100)
    return roll <= chance

def _perception_check(player, threshold=3):
    return int(player.get('stats', {}).get('Percepção', 1)) >= threshold

def _strength_check(player, threshold=4):
    return int(player.get('stats', {}).get('Força', 1)) >= threshold

def _compute_max_hp(player):
    presence = int(player.get('stats', {}).get('Presença', 1))
    return 20 + 5 * presence

def _heal_player(player, amount):
    max_hp = int(player.get('max_hp', _compute_max_hp(player)))
    current = int(player.get('hp', max_hp))
    new = current + int(amount)
    if new > max_hp:
        new = max_hp
    player['hp'] = new
    save_player_data(player)
    return new - current  # actual healed amount

def path_scene(player):
    _ensure_inventory_normalized(player)
    _ensure_rodolfo_flags(player)

    while True:
        print_header()
        print('Você parte da cabana em direção a Villa-Nova. O caminho é seco e o sol castiga.\n')
        print('Durante o caminho, você se depara com uma casa feita de barro; conhece o dono: Rodolfo, um agricultor simples e afável.\n')
        print('Opções:')
        print('1) Seguir para Villa-Nova')
        print('2) Conversar com Rodolfo')
        print('3) Abrir Inventário')
        print('4) Voltar ao Menu')
        choice = input('\nEscolha: ').strip()

        if choice == '1':
            print('\nNo caminho, algo muda: um homem surge das sombras com uma faca...')
            print('Um cangaceiro se aproxima e quer roubar suas coisas!')
            wait_for_enter()
            player = start_combat(player, 'ambush_cangaceiro') or player
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
            _ensure_rodolfo_flags(player)
            print_header()
            if not player['rodolfo_flags']['met']:
                print('Rodolfo ergue a cabeça do trabalho na roça e sorri com rugas gentis.')
                print('"Ah sim garoto! Eu me lembro dele... Sei sim, sente um pouco e fala, o que que tu precisa?"')
                player['rodolfo_flags']['met'] = True
                save_player_data(player)
            else:
                print('Rodolfo te reconhece e acena: "Voltou, menino? Diz aí."')
            wait_for_enter()

            while True:
                print_header()
                print('Você conversa com Rodolfo. O que deseja perguntar?')
                print('1) Perguntar sobre onde seu tio pode estar (informações gerais)')
                print('2) Tentar conseguir suprimentos (comida / kit de reparos)')
                print('3) Perguntar se ele tem munição (cartuchos) para espingarda')
                print('4) Tentar convencê-lo a lhe emprestar/procurar uma proteção (botas / armadura)')
                if _perception_check(player, 3):
                    print('5) Investigar detalhes (percepção alta — tentar descobrir coisas na casa de Rodolfo)')
                print('0) Voltar')

                sub = input('\nEscolha: ').strip()

                if sub == '0':
                    break

                elif sub == '1':
                    print_header()
                    print('Rodolfo coça a barba e fala baixo: "Olhei o Villa-Nova por esses dias, uns homens andavam meio esquisitos. Se for atrás, vai com cuidado."')
                    print('Ele te indica um caminho mais seguro e até te mostra uma pegada recente perto do curral — pode ser pista.')
                    save_player_data(player)
                    wait_for_enter()

                elif sub == '2':
                    if player['rodolfo_flags'].get('gave_food'):
                        print_header()
                        print('Rodolfo: "Já dei o que pude, não tenho mais muito não..."')
                        wait_for_enter()
                        continue

                    print_header()
                    print('Rodolfo rasga um pouco a fera da voz: "Rapaz, a vida tá dura. O que tu precisa, comida ou ferramenta pra conserto?"')
                    print('1) Pedir comida')
                    print('2) Pedir kit de reparo')
                    print('3) Voltar')
                    need = input('\nEscolha: ').strip()
                    if need == '3':
                        continue
                    if need == '1':
                        success = _presence_check(player, difficulty_base=25)
                        if success:
                            print_header()
                            print('Rodolfo suspira e abre um saco velho: "Leva aí, menino. Não é muito, mas te ajuda."')
                            _add_item_to_player(player, 'comida crua', qty=2)
                            # cura imediata entre 5 e 10 HP
                            healed = _heal_player(player, random.randint(5, 10))
                            player['rodolfo_flags']['gave_food'] = True
                            save_player_data(player)
                            print(f'Você foi curado em {healed} HP.')
                            wait_for_enter()
                        else:
                            if _strength_check(player, 4):
                                print_header()
                                print('Rodolfo olhando assustado ante sua postura: "Tá bem... Leva pelo menos um pouco, não mexa comigo não."')
                                _add_item_to_player(player, 'comida crua', qty=1)
                                healed = _heal_player(player, random.randint(5, 10))
                                player['rodolfo_flags']['gave_food'] = True
                                save_player_data(player)
                                print(f'Você foi curado em {healed} HP.')
                                wait_for_enter()
                            else:
                                print_header()
                                print('Rodolfo balança a cabeça: "Desculpa, menino. Não posso te dar mais sem pagamento."')
                                wait_for_enter()

                    elif need == '2':
                        if player['rodolfo_flags'].get('gave_kit'):
                            print_header()
                            print('Rodolfo: "Já te dei um kit. Não tenho outro."')
                            wait_for_enter()
                            continue
                        success = _presence_check(player, difficulty_base=30)
                        if success:
                            print_header()
                            print('Rodolfo: "Ah, essas peças antigas servem. Toma esse kit de reparo que tenho guardado."')
                            kit = {
                                'id': 'kit_reparo',
                                'name': 'Kit de Reparo',
                                'qty': 1,
                                'weight': 1.5,
                                'effects': 'Permite reparar ferramentas simples',
                                'bonus_capacity': 0,
                                'equipable': False,
                                'equipped': False,
                                'slot': None,
                                'damage_min': 0,
                                'damage_max': 0,
                                'ap_cost': 0,
                                'range': 0,
                                'ammo_type': None,
                                'ammo_per_shot': 0,
                                'armor_hp': 0
                            }
                            inv = player.get('inventory', [])
                            inv.append(kit)
                            player['inventory'] = inv
                            player['rodolfo_flags']['gave_kit'] = True
                            save_player_data(player)
                            wait_for_enter()
                        else:
                            print_header()
                            print('Rodolfo: "Eu não guardo essas coisas à toa, menino."')
                            wait_for_enter()
                    else:
                        print('\nEntrada inválida.')
                        wait_for_enter()

                elif sub == '3':
                    if player['rodolfo_flags'].get('gave_ammo'):
                        print_header()
                        print('Rodolfo: "Já te dei o que pude de munição."')
                        wait_for_enter()
                        continue
                    print_header()
                    print('Rodolfo coça a cabeça: "Munição? Tenho alguns cartuchos, mas não é muito."')
                    success = _presence_check(player, difficulty_base=20)
                    if success:
                        print_header()
                        print('Rodolfo entrega alguns cartuchos: "Pegue, mas use com sabedoria."')
                        _add_item_to_player(player, 'cartuchos', qty=3)
                        player['rodolfo_flags']['gave_ammo'] = True
                        save_player_data(player)
                        wait_for_enter()
                    else:
                        if _strength_check(player, 4):
                            print_header()
                            print('Rodolfo apressado: "Tá bom! Leve um só, e sai daqui."')
                            _add_item_to_player(player, 'cartuchos', qty=1)
                            player['rodolfo_flags']['gave_ammo'] = True
                            save_player_data(player)
                            wait_for_enter()
                        else:
                            print_header()
                            print('Rodolfo: "Sinto muito, não posso."')
                            wait_for_enter()

                elif sub == '4':
                    if player['rodolfo_flags'].get('gave_armor'):
                        print_header()
                        print('Rodolfo: "Já dei proteção pra ti, não tenho mais."')
                        wait_for_enter()
                        continue
                    print_header()
                    print('Rodolfo coça a mão: "Botas velhas? Tenho umas botas que seu pai me deixou, topo emprestar se... você me convencer."')
                    if _presence_check(player, difficulty_base=35):
                        print_header()
                        print('Rodolfo entrega um par de botas de couro: "Cuida delas, menino."')
                        _add_item_to_player(player, 'botas de couro', qty=1)
                        player['rodolfo_flags']['gave_armor'] = True
                        save_player_data(player)
                        wait_for_enter()
                    else:
                        if _strength_check(player, 5):
                            print_header()
                            print('Rodolfo olha assustado com tua força e entrega as botas por medo.')
                            _add_item_to_player(player, 'botas de couro', qty=1)
                            player['rodolfo_flags']['gave_armor'] = True
                            save_player_data(player)
                            wait_for_enter()
                        else:
                            print_header()
                            print('Rodolfo: "Não posso, sinto muito. Essas coisas servem a familia..."')
                            wait_for_enter()

                elif sub == '5' and _perception_check(player, 3):
                    print_header()
                    print('Você observa melhor a casa e enxerga sinais de uma caixa trancada atrás do celeiro.')
                    print('Rodolfo, surpreso, dá a chance de abrir — mas pede ajuda para carregar (teste de força).')
                    wait_for_enter()
                    print('Você tenta abrir a caixa...')
                    if _strength_check(player, 3):
                        print('Você abre a caixa e encontra: uma moeda antiga e algumas ferramentas pequenas.')
                        _add_item_to_player(player, 'moeda antiga', qty=1)
                        kit = {
                            'id': 'ferramentas_pequenas',
                            'name': 'Ferramentas Pequenas',
                            'qty': 1,
                            'weight': 0.5,
                            'effects': 'Útil para pequenos reparos',
                            'bonus_capacity': 0,
                            'equipable': False,
                            'equipped': False,
                            'slot': None,
                            'damage_min': 0,
                            'damage_max': 0,
                            'ap_cost': 0,
                            'range': 0,
                            'ammo_type': None,
                            'ammo_per_shot': 0,
                            'armor_hp': 0
                        }
                        inv = player.get('inventory', [])
                        inv.append(kit)
                        player['inventory'] = inv
                        save_player_data(player)
                        wait_for_enter()
                    else:
                        print('A caixa é pesada demais; não consegue abrir sozinho.')
                        wait_for_enter()

                else:
                    print_header()
                    print('Entrada inválida ou opção indisponível.')
                    wait_for_enter()

        elif choice == '3':
            open_inventory(player)

        elif choice == '4':
            return player

        else:
            print('\nEscolha inválida.')
            wait_for_enter()
