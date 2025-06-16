local Calculator = require "calculator"

-- Texto que o usuário digita (ex: "10+2")
local userInput = ""
-- Texto do resultado ou mensagem de erro
local outputText = ""
-- Fonte de texto para exibição
local mainFont

function love.load()
    mainFont = love.graphics.newFont(32)
    love.graphics.setFont(mainFont)
end

-- Captura caracteres digitados que sejam números ou operadores
function love.textinput(character)
    if character:match("[%d%+%-%*/%%%.]") then
        userInput = userInput .. character
    end
end

-- Trata teclas especiais: backspace, enter e escape
function love.keypressed(key)
    if key == "backspace" then
        -- Remove último caractere
        userInput = userInput:sub(1, -2)
    elseif key == "return" or key == "kpenter" then
        -- Avalia expressão ao pressionar Enter
        local result, errorMessage = Calculator.evaluateExpression(userInput)
        if result then
            outputText = "= " .. result
        else
            outputText = errorMessage
        end
    elseif key == "escape" then
        -- Limpa tudo
        userInput = ""
        outputText = ""
    end
end

function love.draw()
    local windowWidth, windowHeight = love.graphics.getDimensions()

    -- Fundo
    love.graphics.clear(0.1, 0.1, 0.1)

    -- Caixa de entrada (borda)
    love.graphics.setColor(1, 1, 1)
    love.graphics.rectangle("line", 50, 50, windowWidth - 100, 60)
    -- Caixa de resultado (borda)
    love.graphics.rectangle("line", 50, 140, windowWidth - 100, 60)

    -- Texto de entrada e resultado
    love.graphics.print("Expressão: " .. userInput, 60,  60)
    love.graphics.print("Resultado: " .. outputText, 60, 150)

    -- Instruções adicionais
    love.graphics.setFont(love.graphics.newFont(16))
    love.graphics.print(
        "Use 0-9 e + - * / % .  |  Enter = calcular  |  Esc = limpar  |  Backspace = apagar",
        50,
        windowHeight - 40
    )
end
