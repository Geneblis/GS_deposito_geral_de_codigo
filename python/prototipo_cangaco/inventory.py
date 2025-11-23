# FILE: inventory.py
import os
import json
import random

from ui import print_header, wait_for_enter
from save_manager import save_player_data

ITEMS_FILE = os.path.join(os.path.dirname(__file__), 'items.json')

def _load_item_catalog():
    try:
        with open(ITEMS_FILE, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
            return {k.lower(): v for k, v in data.items()}
    except Exception:
        return {}

ITEM_CATALOG = _load_item_catalog()

def _normalize_inventory(player):
    inv = player.get('inventory', [])
    normalized = []
    if not inv:
        player['inventory'] = normalized
        return
    if isinstance(inv[0], str):
        for name in inv:
            key = name.lower()
            catalog = ITEM_CATALOG.get(key, None)
            item = {
                'id': key,
                'name': catalog['display'] if catalog else name,
                'qty': 1,
                'weight': float(catalog['weight']) if catalog else 1.0,
                'effects': catalog.get('effects', '') if catalog else '',
                'bonus_capacity': int(catalog.get('bonus_capacity', 0)) if catalog else 0,
                'equipable': bool(catalog.get('equipable', False)) if catalog else False,
                'equipped': False,
                'slot': catalog.get('slot') if catalog else None,
                'damage_min': int(catalog.get('damage_min', 0)) if catalog else 0,
                'damage_max': int(catalog.get('damage_max', 0)) if catalog else 0,
                'ap_cost': int(catalog.get('ap_cost', 0)) if catalog else 0,
                'range': int(catalog.get('range', 0)) if catalog else 0,
                'ammo_type': catalog.get('ammo_type') if catalog else None,
                'ammo_per_shot': int(catalog.get('ammo_per_shot', 0)) if catalog else 0,
                'armor_hp': int(catalog.get('armor_hp', 0)) if catalog else 0
            }
            normalized.append(item)
    else:
        for it in inv:
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
    player['inventory'] = normalized
    save_player_data(player)

def compute_max_capacity(player):
    base_strength = int(player.get('stats', {}).get('Força', 1))
    base_capacity = 10 + base_strength * 10
    bonus = 0
    for it in player.get('inventory', []):
        if it.get('equipped'):
            bonus += int(it.get('bonus_capacity', 0))
    return base_capacity + bonus

def compute_current_load(player):
    total = 0.0
    for it in player.get('inventory', []):
        total += float(it.get('weight', 0.0)) * int(it.get('qty', 1))
    return total

def compute_hp_max(player):
    presence = int(player.get('stats', {}).get('Presença', 1))
    return 20 + 5 * presence + sum(int(it.get('armor_hp', 0)) for it in player.get('inventory', []) if it.get('equipped') and it.get('slot') == 'armor')

def get_equipped_weapon(player):
    for it in player.get('inventory', []):
        if it.get('equipped') and it.get('slot') == 'weapon':
            return it
    return None

def get_equipped_armor(player):
    for it in player.get('inventory', []):
        if it.get('equipped') and it.get('slot') == 'armor':
            return it
    return None

def compute_player_damage_range(player):
    weapon = get_equipped_weapon(player)
    if not weapon:
        return (6, 12)  # unarmed
    dm = int(weapon.get('damage_min', 0))
    dM = int(weapon.get('damage_max', 0))
    if dm <= 0 and dM <= 0:
        # fallback sample damage
        return (5, 10)
    return (dm, dM)

def find_ammo_count(player, ammo_type):
    if not ammo_type:
        return 0
    total = 0
    for it in player.get('inventory', []):
        if it.get('id') == ammo_type:
            total += int(it.get('qty', 1))
    return total

def open_inventory(player):
    _normalize_inventory(player)
    while True:
        print_header()
        player_name = player.get('name', 'SemNome')
        player_level = player.get('level', 1)
        max_capacity = compute_max_capacity(player)
        current_load = compute_current_load(player)
        hp_max = compute_hp_max(player)
        hp_current = int(player.get('hp', player.get('max_hp', hp_max)))
        ap_max = int(player.get('action_points', 8))
        ap_current = int(player.get('current_ap', ap_max))
        coins = int(player.get('coins', 0))
        dmg_min, dmg_max = compute_player_damage_range(player)
        weapon = get_equipped_weapon(player)
        armor = get_equipped_armor(player)

        print(f"{player_name} ---- LVL: {player_level} --- {current_load:.1f}/{max_capacity:.1f}kg")
        print(f"HP: {hp_current}/{hp_max}  ---  AP: {ap_current}/{ap_max}  ---  DANO: [{dmg_min} - {dmg_max}]")
        if weapon:
            ammo_count = find_ammo_count(player, weapon.get('ammo_type'))
            ammo_info = f" (Ammo: {ammo_count})" if weapon.get('ammo_type') else ""
            print(f"\nArma Equipada: {weapon.get('name')}{ammo_info} [{weapon.get('damage_min')} - {weapon.get('damage_max')}] [Alcance: {weapon.get('range')}m] [Peso: {weapon.get('weight')}kg]")
        else:
            print("\nArma Equipada: Socos (6-12 dano) [Alcance: 12m]")

        if armor:
            print(f"Armadura Equipada: {armor.get('name')} [+{armor.get('armor_hp',0)} HP]")
        else:
            print("Armadura Equipada: Nenhuma")

        print(f"\nMoedas: {coins}    Itens: {len(player.get('inventory', []))}\n")

        inv = player.get('inventory', [])
        if not inv:
            print("Inventário vazio.\n")
            wait_for_enter()
            return

        for index, it in enumerate(inv):
            line_prefix = f"{index+1}) "
            qty = int(it.get('qty', 1))
            weight = float(it.get('weight', 0.0))
            effects = it.get('effects', '')
            name = it.get('name', '')
            slot = it.get('slot')
            extra = ""
            if slot == 'weapon':
                extra = f" [W:{it.get('damage_min')}-{it.get('damage_max')} R:{it.get('range')}m AP:{it.get('ap_cost')}]"
                if it.get('ammo_type'):
                    ammo_count = find_ammo_count(player, it.get('ammo_type'))
                    extra += f" (Ammo:{ammo_count})"
            if slot == 'armor':
                extra = f" [ArmorHP:+{it.get('armor_hp',0)}]"
            if it.get('equipped'):
                print(f"{line_prefix}[{name}]{extra} {{{effects}}} ---- ({qty})({weight}kg)")
            else:
                print(f"{line_prefix}{name}{extra} --- ({qty})({weight}kg)")

        print("\n0) Voltar")
        choice = input("\nSelecione um item pelo número para ação (ou 0 para voltar): ").strip()
        try:
            num = int(choice)
        except ValueError:
            print("\nEntrada inválida.")
            wait_for_enter()
            continue

        if num == 0:
            save_player_data(player)
            return

        if not (1 <= num <= len(inv)):
            print("\nNúmero inválido.")
            wait_for_enter()
            continue

        selected = inv[num - 1]
        while True:
            print_header()
            print(f'Selecionado {selected.get("name")}, o que deseja fazer?')
            print("\n1) Equipar/Desequipar")
            print("2) Jogar Fora")
            print("0) Voltar")
            action = input("\nEscolha: ").strip()
            if action == '0':
                break
            if action == '1':
                if not selected.get('equipable'):
                    print("\nEste item não pode ser equipado.")
                    wait_for_enter()
                    continue
                # se for weapon ou armor, garantir apenas um por slot
                slot = selected.get('slot')
                if selected.get('equipped'):
                    selected['equipped'] = False
                    print(f"\n{selected.get('name')} foi desequipado.")
                    save_player_data(player)
                    wait_for_enter()
                    break
                else:
                    if slot:
                        for it in inv:
                            if it.get('equipped') and it.get('slot') == slot:
                                it['equipped'] = False
                    selected['equipped'] = True
                    print(f"\n{selected.get('name')} foi equipado.")
                    save_player_data(player)
                    wait_for_enter()
                    break
            elif action == '2':
                max_drop = int(selected.get('qty', 1))
                if max_drop <= 0:
                    print("\nNada para descartar.")
                    wait_for_enter()
                    break
                print(f"\nQuantas unidades de {selected.get('name')} deseja descartar? (max {max_drop})")
                qty_choice = input("Quantidade: ").strip()
                try:
                    qty_drop = int(qty_choice)
                except ValueError:
                    print("\nEntrada inválida.")
                    wait_for_enter()
                    break
                if qty_drop <= 0 or qty_drop > max_drop:
                    print("\nQuantidade inválida.")
                    wait_for_enter()
                    break
                selected['qty'] = max_drop - qty_drop
                if selected['qty'] <= 0:
                    inv.pop(num - 1)
                print(f"\nVocê descartou {qty_drop}x {selected.get('name')}.")
                save_player_data(player)
                wait_for_enter()
                break
            else:
                print("\nEntrada inválida.")
                wait_for_enter()
                continue
