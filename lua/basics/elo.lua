local x = {'h','e','l','l','o','!'}

-- <index>, elementos, tabela.
for _, i in pairs(x) do
    print(i)
end

local truk = true
while truk do
    print(" ")
    print("Ola!")
    truk = false
end

--  #olha o tamanho de uma tabela.
if not truk and #x > 11 then
    print("This is truk!")
elseif #x <= 6 then
    print("Table X tem " .. #x .. " elementos!")
else
    print("End!")
end
