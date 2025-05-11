local T = { x = 10, y = 20 }
local mt = {}
function mt:__tostring()
  return "(" .. self.x .. "," .. self.y .. ")"
end

-- aplica a metatable a T
setmetatable(T, mt)
print(T)
