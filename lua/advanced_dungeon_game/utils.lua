local utils = {}

-- Divide uma string em palavras (separadas por espaços)
function utils.split(text)
    local words = {}
    for word in text:gmatch("%S+") do
        table.insert(words, word)
    end
    return words
end

-- Retorna uma função que gera IDs únicos (1, 2, 3, …)
function utils.new_id_generator()
    local current = 0
    return function()
        current = current + 1
        return current
    end
end

return utils