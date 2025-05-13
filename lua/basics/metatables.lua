local T = { x = 10, y = 20 }
local mt = {}
function mt:__tostring()
  return "(" .. self.x .. "," .. self.y .. ")"
end

-- aplica a metatable a T
setmetatable(T, mt)
print(T)

-------------------------------------------------------------------
local mapTable = {Mon="Monday", Tue="Tuesday", Wed="Wednesday"}
-- set the metatable
setmetatable(mapTable, {
   -- self represent the table on which metatable is applied
   -- index is the non-existing index
   __index = function(self, index)
    return "Not defined."
   end
})
-- print value using existing key
print(mapTable.Mon)
-- print value using non-exiting key
print(mapTable.Sun)