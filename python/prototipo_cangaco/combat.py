# FILE: combat.py
# Sistema de combate por turnos simples para encontros (módulo separado).
# Uso: from combat import start_combat
# start_combat(player, 'ambush_cangaceiro')

import os
import json
import random
from save_manager import save_player_data
from ui import print_header, wait_for_enter
from inventory import open_inventory  # permite abrir inventário durante combate

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
            # clone to avoid mutating file data
            enemies = []
            for e in encounter:
                enemies.append({
                    'name': e.get('name', 'Inimigo'),
                    'hp': int(e.get('hp', 10)),
                    'atk': int(e.get('atk', 1)),
                    'distance': int(e.get('distance', 6))  # metros
                })
            return enemies
    except Exception:
        return []

def _player_max_hp(player):
    presence = int(player.get('stats', {}).get('Presença', 1))
    return 20 + 5 * presence

def _get_equipped_weapon(player):
    inv = player.get('inventory', [])
    for it in inv:
        if it.get('equipped'):
            return it
    return None

def _weapon_damage_from_catalog(equipped):
    if not equipped:
        return 5  # soco/ataque básico
    item_id = equipped.get('id', '').lower()
    cat = ITEM_CATALOG.get(item_id, {})
    return int(cat.get('damage', cat.get('damage', 5))) if cat else int(equipped.get('damage', 5))

def start_combat(player, encounter_key):
    enemies = _load_encounter(encounter_key)
    if not enemies:
        print_header()
        print('Não há inimigos para este encontro.')
        wait_for_enter()
        return player

    # ensure player hp/action points exist
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
        # check end conditions
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

        # Player turn
        print_header()
        print('=== Combate ===')
        print('Inimigos:')
        for idx, e in enumerate(alive_enemies):
            dist_m = e['distance']
            dist_level = (dist_m + 5) // 6  # cada 6m é um nível
            print(f"{idx+1}) {e['name']} - HP: {e['hp']} - Distância: {dist_m}m (Nível {dist_level})")
        print('\nAliados:')
        print(f"Você - HP: {player.get('hp')}/{player.get('max_hp')}  AP: {player.get('action_points')}")
        print('\nAções:')
        print('1) Atacar')
        print('2) Andar (aproximar 6m, custa 1 AP)')
        print('3) Abrir Inventário')
        print('4) Fugir (tenta se afastar, acaba o encontro)')
        choice = input('\nEscolha: ').strip()

        if choice == '1':
            equipped = _get_equipped_weapon(player)
            weapon_weight = float(equipped.get('weight', 1)) if equipped else 1.0
            ap_cost = int(max(1, round(weapon_weight)))
            if player.get('action_points', 0) < ap_cost:
                print('\nVocê não tem AP suficiente para atacar com o item equipado.')
                wait_for_enter()
                continue
            # escolher inimigo
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
            # calcula chance por distância
            dist_level = (target['distance'] + 5) // 6
            base_chance = 90
            chance = base_chance - (dist_level - 1) * 15
            if chance < 25:
                chance = 25
            roll = random.randint(1, 100)
            player['action_points'] = player.get('action_points', 0) - ap_cost
            damage = _weapon_damage_from_catalog(equipped)
            if roll <= chance:
                target['hp'] = target['hp'] - damage
                print(f'\nAcertou {target["name"]} e causou {damage} de dano.')
                if target['hp'] <= 0:
                    print(f'{target["name"]} caiu.')
                save_player_data(player)
            else:
                print(f'\nVocê errou o ataque (roll {roll} > {chance}).')
            wait_for_enter()

        elif choice == '2':
            # andar: reduz distância de todos inimigos em 6m, gasta 1 AP
            if player.get('action_points', 0) < 1:
                print('\nVocê não tem AP suficiente para andar.')
                wait_for_enter()
                continue
            player['action_points'] = player.get('action_points', 0) - 1
            for e in alive_enemies:
                if e['distance'] > 6:
                    e['distance'] = e['distance'] - 6
                else:
                    e['distance'] = 0
            print('\nVocê andou 6 metros na direção dos inimigos.')
            save_player_data(player)
            wait_for_enter()

        elif choice == '3':
            open_inventory(player)
            # after inventory, reload values in case of changes
            player = player  # already modified by open_inventory via save
            wait_for_enter()

        elif choice == '4':
            # tentativa simplista de fuga: 50% de chance de sucesso
            roll = random.randint(1, 100)
            if roll <= 50:
                print('\nVocê conseguiu fugir do encontro.')
                save_player_data(player)
                wait_for_enter()
                return player
            else:
                print('\nVocê tentou fugir, mas falhou.')
                wait_for_enter()

        else:
            print('\nEntrada inválida.')
            wait_for_enter()
            continue

        # inimigos agem (após a ação do jogador)
        for e in alive_enemies:
            if e['hp'] <= 0:
                continue
            if e['distance'] > 6:
                # inimigo se aproxima
                e['distance'] = e['distance'] - 6
                if e['distance'] < 0:
                    e['distance'] = 0
                print_header()
                print(f'{e["name"]} se aproxima ({e["distance"]}m).')
                wait_for_enter()
            else:
                # ataca o jogador
                dmg = int(e.get('atk', 1))
                player['hp'] = player.get('hp', 0) - dmg
                print_header()
                print(f'{e["name"]} ataca e causa {dmg} de dano. Você tem {player.get("hp", 0)} HP.')
                save_player_data(player)
                wait_for_enter()
                if player.get('hp', 0) <= 0:
                    break

    # fim loop
