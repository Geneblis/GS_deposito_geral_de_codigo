-- player.lua
local Item = require("item")

local Player = {}
Player.__index = Player

function Player.new(name)
  local self = setmetatable({
    name      = name,
    health    = 100,
    inventory = {}
  }, Player)
  return self
end

function Player:add(item)
  table.insert(self.inventory, item)
  print(self.name .. " pegou " .. tostring(item))
end

function Player:show_inventory()
  print("Inventário de " .. self.name .. ":")
  for i, it in ipairs(self.inventory) do
    print("  ", i, tostring(it))
  end
end

-- Coroutine de regeneração lenta
function Player:regen()
  return coroutine.create(function()
    while true do
      if self.health < 100 then
        self.health = math.min(100, self.health + 5)
        print(self.name .. " regenera 5 pontos (HP="..self.health..")")
      end
      coroutine.yield()
    end
  end)
end

return Player
