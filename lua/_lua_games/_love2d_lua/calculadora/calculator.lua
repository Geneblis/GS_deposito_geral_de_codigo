local Calculator = {}

--- Avalia uma expressão matemática passada como string.
-- @param expression (string) Ex: "12 + 3 * 4"
-- @return (number) resultado da expressão ou (nil, string) mensagem de erro
function Calculator.evaluateExpression(expression)
    -- Compila a string em função retornando o valor
    local compiled, compileError = load("return " .. expression)
    if not compiled then
        return nil, "Erro de sintaxe: " .. compileError
    end
    -- Executa a função com pcall para capturar erros de runtime
    local success, result = pcall(compiled)
    if not success then
        return nil, "Erro ao executar: " .. result
    end
    return result
end

return Calculator