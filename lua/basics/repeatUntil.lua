-- print the first non-empty line
local function Repeater()
    local line = "start"
    repeat line = io.read() until line == "stop"
    print(line)
end
Repeater()