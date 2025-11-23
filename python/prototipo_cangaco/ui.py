import os


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def wait_for_enter(prompt='\n\nPressione ENTER para continuar...'):
    try:
        input(prompt)
    except Exception:
        pass


def print_header():
    clear_screen()
    print('RPG - Cangaço (Protótipo de Terminal)')
    print('----------------------------------')
