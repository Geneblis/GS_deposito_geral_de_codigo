math.randomseed(os.time())

local utils   = require("utils")
local Item    = require("item")
local Enemy   = require("enemy")
local Player  = require("player")

-- Cria jogador
io.write("Seu nome: "); local name = io.read()
local player = Player.new(name)
local regen_co = player:regen()

-- Fábrica de inimigos e tabela de salas simples
local make_enemy = Enemy.new_enemy_factory()
local rooms = {
  { desc = "Sala vazia",        enemy = nil },
  { desc = "Armadilha!",        enemy = make_enemy() },
  { desc = "Salão do tesouro",  enemy = make_enemy() },
}

print("\nBem-vindo ao castelo, " .. player.name)

local room_idx = 1
while true do
  -- Avança regeneração
  coroutine.resume(regen_co)

  local room = rooms[room_idx]
  print("\nVocê entra na sala #" .. room_idx .. ": " .. room.desc)

  -- Se há inimigo, combate
  if room.enemy then
    local en = room.enemy
    local patrol_co = Enemy.patrol(en)
    while en.health > 0 and player.health > 0 do
      -- Patrulha
      coroutine.resume(patrol_co)
      -- Escolha do jogador
      print("Ações: (1) atacar  (2) fugir")
      local act = io.read()
      if act == "1" then
        en.health = en.health - 30
        print("Você atinge o " .. en.type .. " (HP inimigo="..en.health..")")
      else
        print("Você foge para a sala anterior.")
        room_idx = math.max(1, room_idx-1)
        break
      end
    end
    if en.health <= 0 then
      print("Você venceu o inimigo e encontra loot!")
      player:add(en.loot)
      room.enemy = nil
    end
    if player.health <= 0 then
      print("Você foi derrotado... Fim de jogo.")
      break
    end
  end

  -- Navegação
  print("Deseja seguir adiante? (s/n)")
  local resp = io.read()
  if resp ~= "s" then break end
  room_idx = math.min(#rooms, room_idx+1)
end

print("\nPartida encerrada.")
player:show_inventory()
