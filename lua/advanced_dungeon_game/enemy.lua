local utils  = require("utils")
local Item   = require("item")

-- Gerador de IDs único
local generate_id = utils.new_id_generator()

-- Módulo de inimigos
local Enemy = {}

--[[
    Retorna uma FUNÇÃO que, quando chamada, cria um novo inimigo
    com ID único, tipo aleatório, vida inicial e loot.
]]
function Enemy.new_enemy_factory()
  local enemy_types = { "Goblin", "Esqueleto", "Aranha" }

  -- Closure que cria um inimigo
  return function()
    -- Escolhe um tipo de inimigo aleatoriamente
    local choice = math.random(1, #enemy_types)
    local enemy_type = enemy_types[choice]

    -- Monta o objeto inimigo
    local new_enemy = {
      id     = generate_id(),
      type   = enemy_type,
      health = 50,
      loot   = Item.new(enemy_type .. " Dente", math.random(1, 10))
    }

    return new_enemy
  end
end

--[[
  patrol:
    Retorna uma coroutine que, a cada resume, imprime que o inimigo está
    patrulhando até que a saúde seja zero, então printa q foi derrotado.
]]
function Enemy.patrol(enemy)
    local co = coroutine.create(function()
        while enemy.health > 0 do
            print("Inimigo " .. enemy.id .. " (" .. enemy.type .. ") patrulha.")
            coroutine.yield()
        end
        print("Inimigo " .. enemy.id .. " foi derrotado.")
    end)
  return co
end

return Enemy