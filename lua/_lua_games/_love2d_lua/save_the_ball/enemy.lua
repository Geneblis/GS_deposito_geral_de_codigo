local love = require "love"

function Enemy()
    local dice = math.random(1,4)
    local lx,ly
    local lradius = 20

    if dice == 1 then
        lx = math.random(lradius, love.graphics.getWidth())
        ly = lradius * 4
    elseif dice == 2 then
        lx = lradius * 4
        ly = math.random(lradius, love.graphics.getHeight())
    elseif dice == 3 then
        lx = math.random(lradius, love.graphics.getWidth())
        ly = love.graphics.getHeight() + (lradius * 4)
    else
        lx = (lradius * 4) + love.graphics.getWidth()
        ly = math.random(lradius, love.graphics.getHeight())
    end

    return {
        level = 1,
        radius = lradius,
        x = lx,
        y = ly,

        move = function (self, player_x, player_y)
            if player_x - self.x > 0 then
                self.x = self.x + self.level
            elseif player_x - self.x < 0 then
                self.x = self.x - self.level
            end

            if player_y - self.y > 0 then
                self.y = self.y + self.level
            elseif player_x - self.y < 0 then
                self.y = self.y - self.level
            end
        end,

        draw = function (self)
            love.graphics.setColor(1,0.5,0.7)
            love.graphics.circle("fill", self.x, self.y, self.radius)
            love.graphics.setColor(1,1,1)
        end
    }
end

return Enemy