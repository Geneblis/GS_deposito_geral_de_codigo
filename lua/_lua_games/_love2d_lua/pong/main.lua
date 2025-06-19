-- configurações
local WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
local PADDLE_SPEED = 300
local BALL_SPEED   = 250
local PADDLE_W, PADDLE_H = 10, 100
local BALL_SIZE    = 10

-- entidades
local player1, player2, ball, score
score = { p1 = 0, p2 = 0 }


function love.load()
    love.window.setMode(WINDOW_WIDTH, WINDOW_HEIGHT)
    love.graphics.setFont(love.graphics.newFont(32))

    -- jogador 1
    player1 = {
        x = 30,
        y = (WINDOW_HEIGHT - PADDLE_H) / 2,
        w = PADDLE_W,
        h = PADDLE_H
    }
    -- jogador 2
    player2 = {
        x = WINDOW_WIDTH - 30 - PADDLE_W,
        y = (WINDOW_HEIGHT - PADDLE_H) / 2,
        w = PADDLE_W,
        h = PADDLE_H
    }

    -- bola
    ball = {
        x  = (WINDOW_WIDTH  - BALL_SIZE) / 2,
        y  = (WINDOW_HEIGHT - BALL_SIZE) / 2,
        w  = BALL_SIZE,
        h  = BALL_SIZE,
        dx = BALL_SPEED,
        dy = BALL_SPEED
    }
    resetBall()
end

-- centraliza e define direção aleatória
function resetBall()
    ball.x  = (WINDOW_WIDTH  - BALL_SIZE) / 2
    ball.y  = (WINDOW_HEIGHT - BALL_SIZE) / 2
    ball.dx = BALL_SPEED * ((math.random() < 0.5) and 1 or -1)
    ball.dy = BALL_SPEED * (math.random() * 2 - 1)
end

function love.update(dt)
    -- movimento jogador 1 (W/S)
    if love.keyboard.isDown('w') then
        player1.y = math.max(0, player1.y - PADDLE_SPEED * dt)
    elseif love.keyboard.isDown('s') then
        player1.y = math.min(WINDOW_HEIGHT - player1.h, player1.y + PADDLE_SPEED * dt)
    end
    -- movimento jogador 2 (↑/↓)
    if love.keyboard.isDown('up') then
        player2.y = math.max(0, player2.y - PADDLE_SPEED * dt)
    elseif love.keyboard.isDown('down') then
        player2.y = math.min(WINDOW_HEIGHT - player2.h, player2.y + PADDLE_SPEED * dt)
    end

    -- movimenta bola
    ball.x = ball.x + ball.dx * dt
    ball.y = ball.y + ball.dy * dt

    -- colisão com topo/baixo
    if ball.y <= 0 or ball.y + ball.h >= WINDOW_HEIGHT then
        ball.dy = -ball.dy
    end

    -- colisão com paddles
    local function collides(a, b)
        return a.x < b.x + b.w and
               a.x + a.w > b.x and
               a.y < b.y + b.h and
               a.y + a.h > b.y
    end
    if collides(ball, player1) then
        ball.dx = -ball.dx
        ball.x  = player1.x + player1.w
    elseif collides(ball, player2) then
        ball.dx = -ball.dx
        ball.x  = player2.x - ball.w
    end

    -- pontuação
    if ball.x < 0 then
        score.p2 = score.p2 + 1
        resetBall()
    elseif ball.x > WINDOW_WIDTH then
        score.p1 = score.p1 + 1
        resetBall()
    end
end

function love.draw()
    -- desenha paddles
    love.graphics.rectangle('fill', player1.x, player1.y, player1.w, player1.h)
    love.graphics.rectangle('fill', player2.x, player2.y, player2.w, player2.h)
    -- desenha bola
    love.graphics.rectangle('fill', ball.x, ball.y, ball.w, ball.h)

    -- desenha placar
    love.graphics.printf(tostring(score.p1), 0, 10, WINDOW_WIDTH/2, 'center')
    love.graphics.printf(tostring(score.p2), WINDOW_WIDTH/2, 10, WINDOW_WIDTH/2, 'center')

    -- instruções
    love.graphics.setFont(love.graphics.newFont(16))
    love.graphics.printf('W/S = Jogador 1 | ↑/↓ = Jogador 2 | Esc = Sair', 0, WINDOW_HEIGHT - 30, WINDOW_WIDTH, 'center')
end

function love.keypressed(key)
    if key == 'escape' then love.event.quit() end
end
