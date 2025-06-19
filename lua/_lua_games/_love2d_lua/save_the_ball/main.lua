-- main.lua

local love = require "love"
local Enemy = require "enemy"
local Button = require "button"

math.randomseed(os.time())

local game = {
    difficulty = 1,
    state = {
        menu    = true,
        paused  = false,
        running = false,
        ended   = false,
    },
    score           = 0,    -- ← pontuação atual
    scoreTimer      = 0,    -- ← acumula dt até 1s
    nextSpawnScore  = 10,   -- ← próximo threshold de spawn
}

-- player table
local player = {
    radius = 20,
    x = 30,
    y = 30
}

local buttons = {
    menu_state = {}
}

-- lista de inimigos
local enemies = {}

local function resetGame()
    -- limpa inimigos e volta ao menu
    enemies = {}
    game.state.menu    = true
    game.state.running = false

    -- reseta score e timers
    game.score          = 0
    game.scoreTimer     = 0
    game.nextSpawnScore = 10
end

local function startNewGame()
    game.state.menu    = false
    game.state.running = true

    -- reseta score e timers no start
    game.score          = 0
    game.scoreTimer     = 0
    game.nextSpawnScore = 10

    -- cria 1º inimigo
    table.insert(enemies, Enemy())
end

function love.mousepressed(x, y, button, istouch, presses)
    if not game.state.running and button == 1 then
        if game.state.menu then
            for _, btn in pairs(buttons.menu_state) do
                btn:checkPressed(x, y, player.radius)
            end
        end
    end
end

function love.load()
    love.window.setTitle("Save the ball!")
    love.mouse.setVisible(false)

    -- botões (ordem não importa com pairs)
    buttons.menu_state.exit_game = Button("Quit", love.event.quit, nil, 120,50)
    buttons.menu_state.play_game = Button("Play", startNewGame, nil, 120,50)
end

function love.update(dt)
    player.x, player.y = love.mouse.getPosition()

    if game.state.running then
        -- atualiza inimigos
        for i = 1, #enemies do
            enemies[i]:move(player.x, player.y)
        end

        -- incrementa timer de score
        game.scoreTimer = game.scoreTimer + dt
        if game.scoreTimer >= 1 then
            game.scoreTimer = game.scoreTimer - 1
            game.score = game.score + 1

            -- a cada múltiplo de nextSpawnScore, spawna mais um
            if game.score >= game.nextSpawnScore then
                table.insert(enemies, Enemy())
                game.nextSpawnScore = game.nextSpawnScore + 10
            end
        end

        -- checa colisões (distância entre centros)
        for _, e in ipairs(enemies) do
            local dx = player.x - e.x
            local dy = player.y - e.y
            local dist = math.sqrt(dx*dx + dy*dy)
            if dist < (player.radius + e.radius) then
                -- reset no contato
                resetGame()
                break
            end
        end
    end
end

function love.draw()
    -- FPS
    love.graphics.printf(
      "FPS: ".. love.timer.getFPS(),
      love.graphics.newFont(16),
      10, love.graphics.getHeight()-30,
      love.graphics.getWidth()
    )

    if game.state.running then
        -- desenha inimigos e jogador
        for i = 1, #enemies do
            enemies[i]:draw()
        end
        love.graphics.circle("fill", player.x, player.y, player.radius)

        -- desenha score no canto superior
        love.graphics.setColor(1,1,1)
        love.graphics.print("Score: "..game.score, 10, 10)

    elseif game.state.menu then
        -- menu com botões
        local y = 70
        for _, btn in pairs(buttons.menu_state) do
            btn:draw(10, y, 10, 20)
            y = y + 50
        end

        -- desenha jogador menor só pra efeito
        love.graphics.circle("fill", player.x, player.y, player.radius / 2)
    end
end
