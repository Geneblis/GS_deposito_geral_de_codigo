local GRID_SIZE    = 3
local CELL_SIZE    = 200
local LINE_WIDTH   = 4
local PADDING      = 50    -- Espaço acima do grid para o placar

local board        = {}    -- board[y][x] = 1 (X), 2 (O), nil
local currentPlayer = 1    -- 1 = X, 2 = O
local score        = { x = 0, o = 0 }
local restartTimer = nil   -- conta regressiva para resetar após vitória

-- inicializa tabuleiro vazio
local function resetBoard()
    board = {}
    for y = 1, GRID_SIZE do
        board[y] = {}
        for x = 1, GRID_SIZE do
            board[y][x] = nil
        end
    end
    currentPlayer = 1
    restartTimer = nil
end

-- checa linhas, colunas e diagonais
local function checkWin()
    -- linhas e colunas
    for i = 1, GRID_SIZE do
        -- linha
        if board[i][1] and board[i][1] == board[i][2] and board[i][2] == board[i][3] then
            return board[i][1]
        end
        -- coluna
        if board[1][i] and board[1][i] == board[2][i] and board[2][i] == board[3][i] then
            return board[1][i]
        end
    end
    -- diagonais
    if board[1][1] and board[1][1] == board[2][2] and board[2][2] == board[3][3] then
        return board[1][1]
    end
    if board[1][3] and board[1][3] == board[2][2] and board[2][2] == board[3][1] then
        return board[1][3]
    end
    -- nenhum vencedor
    return nil
end

-- checa empate
local function isDraw()
    for y = 1, GRID_SIZE do
        for x = 1, GRID_SIZE do
            if not board[y][x] then
                return false
            end
        end
    end
    return true
end

function love.load()
    love.graphics.setLineWidth(LINE_WIDTH)
    resetBoard()
end

function love.update(dt)
    if restartTimer then
        restartTimer = restartTimer - dt
        if restartTimer <= 0 then
            resetBoard()
        end
    end
end

function love.mousepressed(x, y, button)
    if button ~= 1 or restartTimer then return end
    -- traduz clique em coordenada de célula
    local cx = math.floor(x / CELL_SIZE) + 1
    local cy = math.floor((y - PADDING) / CELL_SIZE) + 1
    if cx < 1 or cx > GRID_SIZE or cy < 1 or cy > GRID_SIZE then return end

    if not board[cy][cx] then
        board[cy][cx] = currentPlayer
        -- verifica vitória
        local winner = checkWin()
        if winner then
            if winner == 1 then score.x = score.x + 1
            else                score.o = score.o + 1 end
            restartTimer = 2   -- 2s até reset
        elseif isDraw() then
            restartTimer = 2
        else
            currentPlayer = 3 - currentPlayer  -- alterna 1⇄2
        end
    end
end

function love.draw()
    -- desenha placar
    love.graphics.printf(
        string.format("Placar  X: %d   O: %d", score.x, score.o),
        0, 10, love.graphics.getWidth(), "center"
    )
    -- desenha aviso de vitória
    if restartTimer then
        love.graphics.printf(
            checkWin()
            and string.format("Jogador %s venceu!", checkWin()==1 and "X" or "O")
            or "Empate!",
            0, love.graphics.getHeight()/2 - 20, love.graphics.getWidth(), "center"
        )
    end

    -- desenha grid
    local w, h = love.graphics.getWidth(), love.graphics.getHeight() - PADDING
    love.graphics.translate(0, PADDING)
    for i = 1, GRID_SIZE-1 do
        love.graphics.line(i*CELL_SIZE, 0, i*CELL_SIZE, GRID_SIZE*CELL_SIZE)
        love.graphics.line(0, i*CELL_SIZE, GRID_SIZE*CELL_SIZE, i*CELL_SIZE)
    end

    -- desenha X e O
    for y = 1, GRID_SIZE do
        for x = 1, GRID_SIZE do
            local v = board[y][x]
            if v then
                local px = (x-1)*CELL_SIZE
                local py = (y-1)*CELL_SIZE
                if v == 1 then
                    -- X
                    local margin = 20
                    love.graphics.line(
                        px+margin,       py+margin,
                        px+CELL_SIZE-margin, py+CELL_SIZE-margin
                    )
                    love.graphics.line(
                        px+CELL_SIZE-margin, py+margin,
                        px+margin,       py+CELL_SIZE-margin
                    )
                else
                    -- O
                    love.graphics.circle(
                        "line",
                        px + CELL_SIZE/2,
                        py + CELL_SIZE/2,
                        CELL_SIZE/2 - 20
                    )
                end
            end
        end
    end
end
