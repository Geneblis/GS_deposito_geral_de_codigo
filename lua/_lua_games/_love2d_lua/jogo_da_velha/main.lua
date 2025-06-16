-- ======== Constantes ========
local GRID_SIZE       = 3       -- número de células por linha/coluna
local CELL_SIZE       = 200     -- tamanho em pixels de cada célula
local LINE_THICKNESS  = 4       -- espessura das linhas do tabuleiro
local TOP_MARGIN      = 50      -- espaço em cima para o placar
local RESTART_DELAY   = 2       -- segundos até reiniciar após vitória/empate

-- ======== Estado do Jogo ========
local board           = {}      -- tabuleiro: board[row][col] -> 1 (X), 2 (O) ou nil
local currentPlayer   = 1       -- 1 = X, 2 = O
local score           = {X = 0, O = 0}
local restartTimer    = nil     -- contador para reinício automático

-- ======== Funções Auxiliares ========

-- Reinicia o tabuleiro e o jogador atual
local function resetGame()
    for row = 1, GRID_SIZE do
        board[row] = {}
        for col = 1, GRID_SIZE do
            board[row][col] = nil
        end
    end
    currentPlayer = 1
    restartTimer = nil
end

-- Retorna 1, 2 ou nil se houver vencedor
local function checkWinner()
    -- linhas e colunas
    for i = 1, GRID_SIZE do
        -- linha i
        if board[i][1] and board[i][1] == board[i][2] and board[i][2] == board[i][3] then
            return board[i][1]
        end
        -- coluna i
        if board[1][i] and board[1][i] == board[2][i] and board[2][i] == board[3][i] then
            return board[1][i]
        end
    end
    -- diagonal principal
    if board[1][1] and board[1][1] == board[2][2] and board[2][2] == board[3][3] then
        return board[1][1]
    end
    -- diagonal secundária
    if board[1][3] and board[1][3] == board[2][2] and board[2][2] == board[3][1] then
        return board[1][3]
    end
    return nil
end

-- Retorna true se todas as células estiverem preenchidas
local function isBoardFull()
    for row = 1, GRID_SIZE do
        for col = 1, GRID_SIZE do
            if not board[row][col] then
                return false
            end
        end
    end
    return true
end

-- Converte coordenadas de clique (x, y) para índices de célula (row, col)
local function getCellFromMouse(x, y)
    local col = math.floor(x / CELL_SIZE) + 1
    local row = math.floor((y - TOP_MARGIN) / CELL_SIZE) + 1
    if row < 1 or row > GRID_SIZE or col < 1 or col > GRID_SIZE then
        return nil, nil
    end
    return row, col
end

-- Desenha o placar na parte superior
local function drawScore()
    local text = string.format("Placar — X: %d   O: %d", score.X, score.O)
    love.graphics.printf(text, 0, 10, love.graphics.getWidth(), "center")
end

-- Desenha mensagem de vitória ou empate
local function drawEndMessage()
    if not restartTimer then return end
    local winner = checkWinner()
    local message = winner and (winner == 1 and "Jogador X venceu!" or "Jogador O venceu!") or "Empate!"
    local y = (love.graphics.getHeight() / 2) - 20
    love.graphics.printf(message, 0, y, love.graphics.getWidth(), "center")
end

-- Desenha as linhas do tabuleiro
local function drawGrid()
    love.graphics.translate(0, TOP_MARGIN)
    for i = 1, GRID_SIZE - 1 do
        -- linhas verticais
        love.graphics.line(i * CELL_SIZE, 0, i * CELL_SIZE, GRID_SIZE * CELL_SIZE)
        -- linhas horizontais
        love.graphics.line(0, i * CELL_SIZE, GRID_SIZE * CELL_SIZE, i * CELL_SIZE)
    end
end

-- Desenha X e O nas posições do tabuleiro
local function drawMarks()
    for row = 1, GRID_SIZE do
        for col = 1, GRID_SIZE do
            local cell = board[row][col]
            if cell then
                local px = (col - 1) * CELL_SIZE
                local py = (row - 1) * CELL_SIZE
                local margin = 20
                if cell == 1 then
                    -- X
                    love.graphics.line(px + margin,             py + margin,
                                       px + CELL_SIZE - margin, py + CELL_SIZE - margin)
                    love.graphics.line(px + CELL_SIZE - margin, py + margin,
                                       px + margin,             py + CELL_SIZE - margin)
                else
                    -- O
                    love.graphics.circle("line",
                                         px + CELL_SIZE / 2,
                                         py + CELL_SIZE / 2,
                                         (CELL_SIZE / 2) - margin)
                end
            end
        end
    end
end

-- ======== Callbacks do LÖVE ========

function love.load()
    love.graphics.setLineWidth(LINE_THICKNESS)
    resetGame()
end

function love.update(dt)
    if restartTimer then
        restartTimer = restartTimer - dt
        if restartTimer <= 0 then
            resetGame()
        end
    end
end

function love.mousepressed(x, y, button)
    if button ~= 1 or restartTimer then return end
    local row, col = getCellFromMouse(x, y)
    if not row then return end

    if not board[row][col] then
        board[row][col] = currentPlayer
        local winner = checkWinner()
        if winner then
            if winner == 1 then score.X = score.X + 1 else score.O = score.O + 1 end
            restartTimer = RESTART_DELAY
        elseif isBoardFull() then
            restartTimer = RESTART_DELAY
        else
            currentPlayer = 3 - currentPlayer
        end
    end
end

function love.draw()
    drawScore()
    drawEndMessage()
    drawGrid()
    drawMarks()
end
