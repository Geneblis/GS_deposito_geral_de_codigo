local utils = require("utils")
local Item = {}
Item.__index = Item

-- ID único via closure
local generate_id = utils.new_id_generator()

--[[
  Item.new(name, power):
    Cria um novo item com:
      • id único
      • nome
      • poder (default 0 se não fornecido)
]]
function Item.new(name, power)
  local instance = {
    id    = generate_id(),
    name  = name,
    power = power or 0
  }
  return setmetatable(instance, Item)
end

--[[
  __tostring:
    Define como o item aparece ao usar tostring(item)
    Exemplo: "Espada(#3, Pwr=10)"
]]
function Item:__tostring()
  return string.format("%s(#%d, Pwr=%d)", self.name, self.id, self.power)
end

--[[
  __add:
    Permite usar `item1 + item2` para combinar nomes e somar poderes
    Retorna um novo Item com:
      • nome concatenado: "nome1-nome2"
      • poder = power1 + power2
]]
function Item:__add(other)
  local combined_name  = self.name  .. "-" .. other.name
  local combined_power = self.power + other.power
  return Item.new(combined_name, combined_power)
end

return Item