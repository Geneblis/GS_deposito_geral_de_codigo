# FILE: inventory.py
# Sistema de inventário: carrega catálogo de items de items.json,
# exibição, equipar/descartar, cálculo de carga e HP.
# Salva alterações chamando save_player_data(player).

import os
import json

from ui import print_header, wait_for_enter
from save_manager import save_player_data

# Arquivo JSON com catálogo de itens
ITEMS_FILE = os.path.join(os.path.dirname(__file__), 'items.json')

def _load_item_catalog():
    try:
        with open(ITEMS_FILE, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
            # garante chaves em lowercase
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
    # se inventário é lista de strings, converte usando catálogo
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
                'equipped': False
            }
            normalized.append(item)
    else:
        # assume já está normalizado (lista de dicts). garante chaves e tipos.
        for it in inv:
            item = dict(it)
            item.setdefault('id', item.get('name', '').lower())
            item.setdefault('qty', int(item.get('qty', 1)))
            item.setdefault('weight', float(item.get('weight', 1.0)))
            item.setdefault('effects', item.get('effects', ''))
            item.setdefault('bonus_capacity', int(item.get('bonus_capacity', 0)))
            item.setdefault('equipable', bool(item.get('equipable', False)))
            item.setdefault('equipped', bool(item.get('equipped', False)))
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

def compute_hp(player):
    presence = int(player.get('stats', {}).get('Presença', 1))
    return 20 + 5 * presence

def open_inventory(player):
    _normalize_inventory(player)
    while True:
        print_header()
        player_name = player.get('name', 'SemNome')
        player_level = player.get('level', 1)
        max_capacity = compute_max_capacity(player)
        current_load = compute_current_load(player)
        hp = compute_hp(player)

        print(f"{player_name} ---- LVL: {player_level} --- {current_load:.1f}/{max_capacity:.1f}kg")
        print(f"HP Máx: {hp}  |  Itens: {len(player.get('inventory', []))}\n")

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
            if it.get('equipped'):
                print(f"{line_prefix}[{name}] {{{effects}}} ---- ({qty})({weight}kg)")
            else:
                print(f"{line_prefix}{name} --- ({qty})({weight}kg)")

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
        # prompt actions
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
                # alterna equip
                if selected.get('equipped'):
                    selected['equipped'] = False
                    print(f"\n{selected.get('name')} foi desequipado.")
                    save_player_data(player)
                    wait_for_enter()
                    break
                else:
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
