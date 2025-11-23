import os
import json
import random
from save_manager import save_player_data
from ui import print_header, wait_for_enter
from inventory import open_inventory, get_equipped_weapon, get_equipped_armor

ITEMS_FILE = os.path.join(os.path.dirname(__file__), 'items.json')
ENEMIES_FILE = os.path.join(os.path.dirname(__file__), 'enemies.json')

def _load_items():
    try:
        with open(ITEMS_FILE, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
            return {k.lower(): v for k, v in data.items()}
    except Exception:
        return {}

ITEM_CATALOG = _load_items()

def _load_encounter(encounter_key):
    try:
        with open(ENEMIES_FILE, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
            encounter = data.get(encounter_key, [])
            enemies = []
            for e in encounter:
                enemies.append({
                    'name': e.get('name', 'Inimigo'),
                    'hp': int(e.get('hp', 10)),
                    'atk': int(e.get('atk', 1)),
                    'distance': int(e.get('distance', 6)),
                    'ap': int(e.get('ap', 4)),
                    'weapon': e.get('weapon')  # id string or null
                })
            return enemies
    except Exception:
        return []

def _player_max_hp(player):
    presence = int(player.get('stats', {}).get('Presença', 1))
    return 20 + 5 * presence

def _weapon_stats_from_item(item):
    if not item:
        return None
    item_id = item.get('id', '').lower()
    cat = ITEM_CATALOG.get(item_id, {})
    stats = {
        'damage_min': int(item.get('damage_min', cat.get('damage_min', 0))),
        'damage_max': int(item.get('damage_max', cat.get('damage_max', 0))),
        'ap_cost': int(item.get('ap_cost', cat.get('ap_cost', 0))),
        'range': int(item.get('range', cat.get('range', 0))),
        'weight': float(item.get('weight', cat.get('weight', 1.0))),
        'ammo_type': item.get('ammo_type', cat.get('ammo_type')),
        'ammo_per_shot': int(item.get('ammo_per_shot', cat.get('ammo_per_shot', 0)))
    }
    return stats

def _unarmed_damage():
    roll = random.randint(1, 20)
    if roll == 20:
        return 12  # critical
    return random.randint(6, 12)

def _has_ammo(player, ammo_type, needed):
    if not ammo_type:
        return True
    total = 0
    for it in player.get('inventory', []):
        if it.get('id') == ammo_type:
            total += int(it.get('qty', 1))
    return total >= needed

def _consume_ammo(player, ammo_type, qty):
    if not ammo_type or qty <= 0:
        return
    inv = player.get('inventory', [])
    for it in inv:
        if it.get('id') == ammo_type:
            have = int(it.get('qty', 1))
            take = min(have, qty)
            it['qty'] = have - take
            qty -= take
            if it['qty'] <= 0:
                inv.remove(it)
            if qty <= 0:
                break
    player['inventory'] = inv
    save_player_data(player)

def start_combat(player, encounter_key):
    enemies = _load_encounter(encounter_key)
    if not enemies:
        print_header()
        print('Não há inimigos para este encontro.')
        wait_for_enter()
        return player

    if 'hp' not in player or player.get('hp') is None:
        player['hp'] = _player_max_hp(player)
    if 'max_hp' not in player or player.get('max_hp') is None:
        player['max_hp'] = _player_max_hp(player)
    if 'action_points' not in player or player.get('action_points') is None:
        agility = int(player.get('stats', {}).get('Agilidade', 1))
        player['action_points'] = 8 + agility * 2

    print_header()
    print('Um inimigo se aproxima! Prepare-se para o combate.')
    wait_for_enter()

    while True:
        alive_enemies = [e for e in enemies if e['hp'] > 0]
        if not alive_enemies:
            print_header()
            print('Todos os inimigos foram derrotados.')
            save_player_data(player)
            wait_for_enter()
            return player
        if player.get('hp', 0) <= 0:
            print_header()
            print('Você foi derrotado... Fim do combate.')
            player['hp'] = 0
            save_player_data(player)
            wait_for_enter()
            return player

        # start round: restore AP for player and enemies for this round
        player_current_ap = int(player.get('action_points', 0))
        for e in enemies:
            e['current_ap'] = int(e.get('ap', 4))

        # Player phase: can act while player_current_ap > 0
        while player_current_ap > 0 and player.get('hp', 0) > 0:
            print_header()
            print('=== Combate (Sua vez) ===')
            alive_enemies = [e for e in enemies if e['hp'] > 0]
            for idx, e in enumerate(alive_enemies):
                dist_m = e['distance']
                dist_level = (dist_m + 5) // 6
                print(f"{idx+1}) {e['name']} - HP: {e['hp']} - Distância: {dist_m}m (Nível {dist_level})")
            print('\nVocê:')
            print(f"HP: {player.get('hp')}/{player.get('max_hp')}  AP disponível (rodada): {player_current_ap}")
            print('\nAções (AP dispon.):')
            print('1) Atacar')
            print('2) Avançar 6m (custa 1 AP)')
            print('5) Recuar 6m (custa 1 AP)')
            print('3) Abrir Inventário (custa 4 AP)')
            print('4) Fugir (tenta terminar encontro)')
            print('0) Terminar sua fase')
            choice = input('\nEscolha: ').strip()

            if choice == '1':
                weapon = get_equipped_weapon(player)
                weapon_stats = _weapon_stats_from_item(weapon) if weapon else None
                if weapon_stats and weapon_stats.get('ammo_type'):
                    if not _has_ammo(player, weapon_stats['ammo_type'], weapon_stats['ammo_per_shot']):
                        print('\nSem munição para esta arma.')
                        wait_for_enter()
                        continue
                if weapon_stats:
                    ap_cost = weapon_stats.get('ap_cost', max(1, int(round(weapon_stats.get('weight', 1)))))
                    w_range = weapon_stats.get('range', 0)
                    dmg_min = weapon_stats.get('damage_min', 0)
                    dmg_max = weapon_stats.get('damage_max', 0)
                else:
                    ap_cost = 1
                    w_range = 12
                    dmg_min = dmg_max = None

                if player_current_ap < ap_cost:
                    print(f'\nAP insuficiente para atacar (precisa {ap_cost}, tem {player_current_ap}).')
                    wait_for_enter()
                    continue

                sel = input('\nEscolha o número do inimigo a atacar: ').strip()
                try:
                    sel_idx = int(sel) - 1
                except ValueError:
                    print('\nEntrada inválida.')
                    wait_for_enter()
                    continue
                if not (0 <= sel_idx < len(alive_enemies)):
                    print('\nInimigo inválido.')
                    wait_for_enter()
                    continue
                target = alive_enemies[sel_idx]

                dist_level = (target['distance'] + 5) // 6
                perception = int(player.get('stats', {}).get('Percepção', 1))
                weight = float(weapon.get('weight', 1)) if weapon else 1.0

                chance = 50 + perception * 5 - (dist_level - 1) * 15 - int(round(weight))
                if chance < 5:
                    chance = 5
                if chance > 95:
                    chance = 95

                roll = random.randint(1, 100)
                player_current_ap -= ap_cost

                # determine damage
                if weapon_stats:
                    # critical if within (weapon range + 12) as requested
                    critical_threshold = weapon_stats.get('range', 0) + 12
                    critical = target['distance'] <= critical_threshold and roll <= max(5, perception * 2)
                    if roll <= chance:
                        if critical:
                            damage = weapon_stats.get('damage_max', weapon_stats.get('damage_min', 1))
                        else:
                            damage = random.randint(weapon_stats.get('damage_min', 1), weapon_stats.get('damage_max', weapon_stats.get('damage_min', 1)))
                        if weapon_stats.get('ammo_type'):
                            _consume_ammo(player, weapon_stats.get('ammo_type'), weapon_stats.get('ammo_per_shot', 1))
                        target['hp'] -= damage
                        print(f'\nAcertou {target["name"]} e causou {damage} de dano. (roll {roll} <= {chance})')
                        if target['hp'] <= 0:
                            print(f'{target["name"]} caiu.')
                        save_player_data(player)
                    else:
                        print(f'\nVocê errou o ataque (roll {roll} > {chance}).')
                else:
                    # unarmed: d20 damage
                    roll20 = random.randint(1, 20)
                    damage = _unarmed_damage()
                    if target['distance'] <= 12 and roll <= chance:
                        target['hp'] -= damage
                        print(f'\nAcertou {target["name"]} com soco e causou {damage} de dano.')
                        if target['hp'] <= 0:
                            print(f'{target["name"]} caiu.')
                        save_player_data(player)
                    else:
                        print('\nFora de alcance para soco ou erro no ataque.')
                wait_for_enter()
                # loop continues while player_current_ap > 0

            elif choice == '2':
                if player_current_ap < 1:
                    print('\nAP insuficiente para avançar.')
                    wait_for_enter()
                    continue
                player_current_ap -= 1
                for e in enemies:
                    e['distance'] = max(0, e['distance'] - 6)
                print('\nVocê avançou 6m.')
                save_player_data(player)
                wait_for_enter()

            elif choice == '5':
                if player_current_ap < 1:
                    print('\nAP insuficiente para recuar.')
                    wait_for_enter()
                    continue
                player_current_ap -= 1
                for e in enemies:
                    e['distance'] += 6
                print('\nVocê recuou 6m.')
                save_player_data(player)
                wait_for_enter()

            elif choice == '3':
                if player_current_ap < 4:
                    print('\nVocê precisa de 4 AP para abrir o inventário durante combate.')
                    wait_for_enter()
                    continue
                player_current_ap -= 4
                open_inventory(player)
                save_player_data(player)
                wait_for_enter()

            elif choice == '4':
                roll_f = random.randint(1, 100)
                if roll_f <= 50:
                    print('\nVocê conseguiu fugir do encontro.')
                    save_player_data(player)
                    wait_for_enter()
                    return player
                else:
                    print('\nFalhou na fuga.')
                    wait_for_enter()

            elif choice == '0':
                break

            else:
                print('\nEntrada inválida.')
                wait_for_enter()
                continue

        # enemy phase: each enemy acts using its own AP pool
        for e in enemies:
            e_ap = int(e.get('current_ap', e.get('ap', 4)))
            while e_ap > 0 and e['hp'] > 0 and player.get('hp', 0) > 0:
                if e['distance'] > 6:
                    e['distance'] = max(0, e['distance'] - 6)
                    print_header()
                    print(f'{e["name"]} se aproxima ({e["distance"]}m).')
                    wait_for_enter()
                    e_ap -= 1
                else:
                    dmg = int(e.get('atk', 1))
                    player['hp'] = player.get('hp', 0) - dmg
                    print_header()
                    print(f'{e["name"]} ataca e causa {dmg} de dano. Você tem {player.get("hp", 0)} HP.')
                    save_player_data(player)
                    wait_for_enter()
                    e_ap -= 1
            e['current_ap'] = e_ap

        # end of round - restore player's AP for next round (use base action_points)
        # player gets full AP each round
        player['current_ap'] = int(player.get('action_points', 0))
        save_player_data(player)