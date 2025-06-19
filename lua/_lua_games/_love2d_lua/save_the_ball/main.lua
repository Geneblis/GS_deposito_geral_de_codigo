--[[
NOTE: I stopped following the tutorial on the point system mechanics. This is not a game rn, more or less an proof of concept, maybe even less...
So if I ever decide to continue, just check this video on the timestamp.
https://youtu.be/mbJlh-7zuqg?si=TqEdWW8Rr0Bq1X3v&t=5573
]]--

local love = require "love"
local Enemy = require "enemy"
local Button = require "button"

math.randomseed(os.time())

local game = {
    difficulty = 1,
    state = {
        menu = true,
        paused = false,
        running = false,
        ended = false,
    }
}

--player table
local player = {
    radius = 20,
    x = 30,
    y = 30
}

local buttons = {
    menu_state = {}
}

--enemy table
local enemies = {}

local function startNewGame()
    game.state["menu"] = false
    game.state["running"] = true

    table.insert(enemies, 1, Enemy())
end

function love.mousepressed(x, y, button, istouch, presses)
    if not game.state["running"] then
        if button == 1 then
            if game.state["menu"] then
                for index in pairs(buttons.menu_state) do
                    buttons.menu_state[index]:checkPressed(x, y, player.radius)
                end
            end
        end
    end
end

function love.load()
    love.window.setTitle("Save the ball!")

    love.mouse.setVisible(false)

    --botoes, ordem de tras pra frente devido ao loop.
    buttons.menu_state.exit_game = Button("Quit", love.event.quit, nil, 120,50)
    buttons.menu_state.play_game = Button("Play", startNewGame, nil, 120,50)
end

function love.update()
    player.x, player.y = love.mouse.getPosition()

    if game.state["running"] then
        for i = 1, #enemies do
            enemies[i]:move(player.x,player.y)
        end        
    end
end

function love.draw()
    love.graphics.printf("FPS: ".. love.timer.getFPS(), love.graphics.newFont(16), 10, love.graphics.getHeight()-30, love.graphics.getWidth())

    if game.state.running then
        for i = 1, #enemies do
            enemies[i]:draw()
        end
        love.graphics.circle("fill", player.x, player.y, player.radius)

    elseif game.state.menu then
        local y = 70
        for idx, btn in pairs(buttons.menu_state) do
            btn:draw(10, y, 10, 20)
            y = y + 50
        end
    end

    if not game.state.running then
        love.graphics.circle("fill", player.x, player.y, player.radius / 2)
    end
end
