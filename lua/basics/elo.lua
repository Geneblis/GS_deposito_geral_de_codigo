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

--funcao anonima
local addler = function (y, z)
    return y + z
end

addler(10,50)

--tabela/array avançada.
local arr = {
    {1,2,3},
    {4,5,6},
    {7,8,9},
}
for i = 1, #arr do
    table.insert(arr[1], 1, 300)
    for j = 1, #arr[i] do
        print(arr[i][j])
    end
end
table.remove(arr, 1) --remove a linha.
print(arr)
table.remove(arr[1], 3) --remove o elemento da linha. #6 pq são 2*3, se eu por arr[2] ele remove o #9 pq agr só existem 2 linhas.
for i = 1, #arr do
    --table.insert(arr[1], 1, 300)
    for j = 1, #arr[i] do
        print(arr[i][j])
    end
end

local function listamento(...)
    local sums = 0

    for key, value in pairs({...}) do
        print(key, value)
    end
    return "FINALIZED."
end

print(listamento(99,1023,3013,39051,0891,2846,18940,1934))


--corrutines
