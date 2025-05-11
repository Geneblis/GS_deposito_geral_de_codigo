local function imprime()
    print("Calculando...")
end

local function soma(a, b)
    io.write("Soma de n1+n2 = ")
    print(a + b)
end

local function divisao(a, b)
    io.write("Divisao de n1/n2 = ")
    if b == 0 then
        print("Deu ruim.")
    else
        print(a / b)
    end
end


io.write("Insira o primeiro valor: ")
local n3 = tonumber(io.read())
io.write("Insira o segundo valor: ")
local n4 = tonumber(io.read())
imprime()
soma(n3, n4)
divisao(n3, n4)
