math.randomseed(os.time())

local score = 0

print("Bem-vindo ao Desafio Matemático!")
print("Você terá que resolver 5 operações básicas.")

for i = 1, 5 do
    local a = math.random(1, 20)
    local b = math.random(1, 20)
    local op = math.random(1, 2)
    local resposta_certa

    if op == 1 then
        print(i .. ") Quanto é " .. a .. " + " .. b .. "?")
        resposta_certa = a + b
    else
        print(i .. ") Quanto é " .. a .. " - " .. b .. "?")
        resposta_certa = a - b
    end

    local resposta = tonumber(io.read())
    if resposta == resposta_certa then
        print("Correto!\n")
        score = score + 1
    else
        print("Errado! A resposta certa era " .. resposta_certa .. "\n")
    end
end

print("Fim do jogo. Você acertou " .. score .. " de 5.")
