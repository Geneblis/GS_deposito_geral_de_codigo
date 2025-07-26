import configparser
import shlex
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INI_PATH = os.path.join(BASE_DIR, "config.ini")

def load_config():
    parser = configparser.ConfigParser()
    parser.read(INI_PATH)
    return parser

def save_config(parser):
    with open(INI_PATH, 'w') as f:
        parser.write(f)

def process_command(line, config):
    tokens = shlex.split(line)
    if not tokens:
        return config

    cmd = tokens[0].lower()
    if cmd == "exit":
        sys.exit()
    elif cmd == "help":
        print_help()
    elif cmd == "get":
        handle_get(tokens, config)
    elif cmd == "set":
        handle_set(tokens, config)
    elif cmd == "delkey":
        handle_delete_key(tokens, config)
    elif cmd == "delsec":
        handle_delete_section(tokens, config)
    else:
        print(f"Comando desconhecido: '{cmd}'. Digite 'help' para ver os comandos.")
    return config

def handle_get(tokens, cfg):
    if len(tokens) == 1:
        for section in cfg.sections():
            print(f"[{section}]")
            for k, v in cfg[section].items():
                print(f"{k} = {v}")
            print()
    elif len(tokens) == 2:
        section = tokens[1]
        if section in cfg:
            for k, v in cfg[section].items():
                print(f"{k} = {v}")
        else:
            print(f"Seção '{section}' não existe")
    elif len(tokens) == 3:
        section, key = tokens[1], tokens[2]
        if section in cfg and key in cfg[section]:
            print(cfg[section][key])
        else:
            print(f"Chave '{key}' na seção '{section}' não encontrada")
    else:
        print("Uso: get [seção] [chave]")

def handle_set(tokens, cfg):
    if len(tokens) != 4:
        print("Uso: set <seção> <chave> <valor>")
        return
    section, key, value = tokens[1], tokens[2], tokens[3]
    if section not in cfg:
        cfg[section] = {}
    cfg[section][key] = value
    save_config(cfg)
    print("OK")

def handle_delete_key(tokens, cfg):
    if len(tokens) != 3:
        print("Uso: delkey <seção> <chave>")
        return
    section, key = tokens[1], tokens[2]
    if section in cfg and key in cfg[section]:
        del cfg[section][key]
        save_config(cfg)
        print("OK")
    else:
        print(f"Chave '{key}' na seção '{section}' não existe")

def handle_delete_section(tokens, cfg):
    if len(tokens) != 2:
        print("Uso: delsec <seção>")
        return
    section = tokens[1]
    if section in cfg:
        del cfg[section]
        save_config(cfg)
        print("OK")
    else:
        print(f"Seção '{section}' não existe")

def print_help():
    print("""
Comandos disponíveis:
  get            — listar todas as seções e chaves
  get <sec>      — listar todas as chaves de <sec>
  get <sec> <key>— mostrar valor de <key> em <sec>
  set <sec> <key> <val> — criar/atualizar
  delkey <sec> <key>    — deletar chave
  delsec <sec>          — deletar seção
  help           — mostrar esta ajuda
  exit           — sair
""".strip())

def interactive_shell():
    cfg = load_config()
    print(f"INI Shell iniciado para: {INI_PATH}")
    print_help()
    while True:
        try:
            line = input("ini> ")
            cfg = process_command(line, cfg)
        except Exception as e:
            print("Erro:", e)

if __name__ == "__main__":
    interactive_shell()
